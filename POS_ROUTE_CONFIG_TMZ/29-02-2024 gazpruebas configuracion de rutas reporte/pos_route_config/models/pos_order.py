from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
import random
import json
import urllib.request


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # _sql_constraints = [
    #     ('gas_ref_unique', 'unique(note,distribution_point_name)',
    #      'There can only be one reference per distribution point name')]

    distribution_point_name = fields.Char(string='Distribution point name', related='config_id.distribution_point_name')
    total_lt = fields.Float(string='Total liters', compute='_compute_total_lt', help="Total gas liters sold by POS", digits= (12,4))
    ref_gaspar = fields.Char(string='Gaspar reference', compute="_get_ref_note")
    total_lt_gas = fields.Float(string='Total liters Gaspar', help="Total gas liters sold by g4s", digits= (12,4))
    hg = fields.Float(string='Hg')
    gaspar_conciliated = fields.Boolean(string='Gaspar conciliated', default=False)    

    
    def _get_ref_note(self):
        for order in self:
            order.ref_gaspar = order.note

    def _compute_total_lt(self):
        for order in self:
            order.total_lt = 0
            order_lines = order.lines
            for line in order_lines:
                if(line.product_id.product_tmpl_id.uom_id.name.upper() == 'KG'):
                    order.total_lt += (line.qty/0.54)
                if(line.product_id.product_tmpl_id.uom_id.name.upper() == 'LT'):
                    order.total_lt += line.qty
                if(line.product_id.product_tmpl_id.uom_id.name.upper() == 'UNIDADES'):
                    if line.product_id.product_tmpl_id.qty_contents:
                        order.total_lt += ((line.qty*line.product_id.product_tmpl_id.qty_contents)/0.54)

    @api.depends('hg', 'total_lt')
    def _compute_total_lt_gaspar(self):
        for order in self:
            order.total_lt_gas = order.total_lt * order.hg

    def get_refunds(self):
        refunds = {}
        for order in self:
            if 'REFUND' in order.name or 'REEMBOLSO' in order.name:
                refunds[order.pos_reference] = order
        return refunds

    def action_manual_conciliate_order(self):
        if not self.session_id.config_id.is_gaspar_available:
            return
        route = self.env['pos_route_config.route_config'].search([('pos_config_id', '=', self.session_id.config_id.id), ('state', '!=', 'finish')])
        if route.state != 'reception':
            raise UserError(_("Can't conciliate gaspar orders until current route configuration is in state 'Route Reception'"))
        for order in self:
            if order.hg and order.total_lt_gas:
                order.gaspar_conciliated = True

    def action_conciliate_orders(self):
        session = self.session_id
        config = session.config_id
        if not config.is_gaspar_available:
            return
        route = self.env['pos_route_config.route_config'].search([('pos_config_id', '=', session.config_id.id), ('state', '!=', 'finish')])
        if route.state != 'reception':
            raise UserError(_("Can't conciliate gaspar orders until current route configuration is in state 'Route Reception'"))
        refunds = self.get_refunds()
        for order in self:
            if order.note and order.pos_reference not in refunds.keys():
                if order.hg and order.total_lt_gas:
                    t = order.total_lt_gas / order.hg * 100
                    dif = t - order.total_lt
                    if dif > 0.1 or dif < -0.1:
                        raise ValidationError(_("Total liters do not match gaspar total liters for order %s", order.name))
                    order.gaspar_conciliated = True
        # TODO cambiar estatus de la ruta a conciliación

    def get_gaspar_data(self):
        try:
            session = self.session_id
            config = session.config_id
            if not config.is_gaspar_available:
                raise UserError(_("Activate gaspar unit in POS settings before trying to fetch gaspar data"))
            distributionPointName = ''
            params = {'serverName': self.env.company.gaspar_server.external_id, 'references': []}
            url = gas_api_url = self.env['ir.config_parameter'].get_param('pos_route_config.gas_api_url') + 'sale'
            refunds = self.get_refunds()
            for order in self:
                distributionPointName = order.config_id.distribution_point_name
                if order.pos_reference not in refunds.keys():
                    params['references'].append(int(order.note.strip()))
            if not distributionPointName:
                raise UserError(_('A valid distribution point name must be configured first'))
            params['distributionPointName'] = distributionPointName
            req = urllib.request.Request(url=url, data=json.dumps(params).encode(),
                headers={"Content-Type": "application/json"}, method='GET')
            decodedResponse = urllib.request.urlopen(req).read().decode()
            res = json.loads(decodedResponse)
            refs = {}
            if res['code'] in (400, 500):
                raise UserError(res['message'])
            for sale in res['result']:
                if sale['sales_folio'] in refs.keys():
                    refs[sale['sales_folio']]['total_volume'] += sale['total_volume']
                else:    
                    refs[sale['sales_folio']] = sale
            for order in self:
                if order.note:
                    if order.note.strip() in refs.keys():
                        order.hg = refs[order.note.strip()]['scheme']
                        order.total_lt_gas = refs[order.note.strip()]['total_volume']
                        if order.total_lt < 0:
                            order.total_lt_gas *= -1
        except Exception as e:
            if isinstance(e, UserError):
                raise e
            raise Warning(_("Unable to fetch gaspar data, try again later"))
