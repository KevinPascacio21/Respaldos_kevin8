from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_round
import logging
_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = 'pos.session'

    can_close_session = fields.Boolean(string='Can close POS session?', default=False)
    gaspar_orders_cons = fields.Boolean(string='Conciliated gaspar orders', compute="_is_gaspar_conciliated")
    total_lt = fields.Float(string='Total liters', compute="_compute_total_lt")
    total_kg = fields.Float(string='Total kilos', compute="_compute_total_kg") 

    def _compute_total_lt(self):
        for session in self:
            session.total_lt = 0.00
            litros_totales = 0.00
            orders = self.env['pos.order'].search([('session_id', '=', session.id)])
            if orders:
                for order in orders:
                    litros_totales += order.total_lt
                    # session.total_lt += order.total_lt
                if len(orders) > 0:
                    session.total_lt = float_round(litros_totales, precision_digits=2, precision_rounding=None)

    def _compute_total_kg(self):
        for session in self:
            session.total_kg = 0.00
            kilos_totales = 0.00
            orders = self.env['pos.order'].search([('session_id', '=', session.id)])
            if orders:
                for order in orders:
                    kilos_totales += order.total_kilos
                    # session.total_kg += order.total_kilos
                if len(orders):
                    session.total_kg = float_round(kilos_totales, precision_digits=2, precision_rounding=None)

    @api.constrains('config_id')
    def _is_new_session_allowed(self):
        for session in self:
            config = self.env['pos.config'].sudo().search([('id', '=', session.config_id.id)])
            if config:
                if not config.can_start_session:
                    raise ValidationError(_("Can't start a session until a route configuration is done"))
        return True
        
    @api.constrains('state')
    def _close_session(self):
        for session in self:
            config = self.env['pos_route_config.route_config'].search([('pos_config_id', '=', session.config_id.id), ('state', '!=', 'finish')])
            if session.state == 'opened':
                config.state = 'sale'
                config.session_id = session
                self.env['pos_route_config.route_config'].sudo().write([config])
            if session.state == 'closed':
                # if not session.gaspar_orders_cons:
                #     raise ValidationError(_("POS orders must be conciliated before closing session"))
                config.state = 'finish'
                config.refuel_state = 'paid'
                if not session.config_id.internal_transfer: 
                    liq_val = {}
                    for liq in self.config_id.liquidacion:
                        # _logger.info(liq.name)
                        if liq.name == "Litrómetro":
                            liq_val[liq.name] = config.dif_volume_meter
                        elif liq.name == "Porcentaje":
                            liq_val[liq.name] = config.dif_percent
                        elif liq.name == "Báscula":
                            liq_val[liq.name] = config.dif_weight
                        elif not self.pos_config_id.liquidacion:
                            liq_val["Portátil"] = config.dif_weight
                    # _logger.info(liq_val)
                    higher_value = 0
                    if len(liq_val) > 0:
                        # _logger.info(liq_val.get(max(liq_val, key=liq_val.get)))
                        higher_value = float_round(liq_val.get(max(liq_val, key=liq_val.get)), precision_digits=2, precision_rounding=None)
                    if 'Portátil' in liq_val.keys():
                        if  float_round(session.total_kg, precision_digits=2, precision_rounding=None) != higher_value:
                            if session.total_kg < (higher_value - 0.5) or session.total_kg > (higher_value + 0.5):
                                raise UserError(_("Sold kilograms do not match difference from starting and ending kilograms")) 
                    else:
                        lt_extra_check = self.env.company.licensed_litros_extra
                        _logger.info('Litrómetro' in liq_val.keys())
                        _logger.info(lt_extra_check)
                        if 'Litrómetro' in liq_val.keys() and lt_extra_check:
                            _logger.info('Entro lt extra')
                            if session.total_lt < (higher_value - 0.5):
                                raise UserError(_("Sold liters do not match difference from starting and ending volume meter"))
                        else:
                            _logger.info('No entro lt extra')
                            if  float_round(session.total_lt, precision_digits=2, precision_rounding=None) != higher_value:
                                if session.total_lt < (higher_value - 0.5) or session.total_lt > (higher_value + 0.5):
                                    if 'Litrómetro' in liq_val.keys():
                                        raise UserError(_("Sold liters do not match difference from starting and ending volume meter"))
                                    elif 'Porcentaje' in liq_val.keys():                        
                                        raise UserError(_("Sold liters do not match difference from starting and ending percentage"))
                                    elif 'Báscula' in liq_val.keys():
                                        raise UserError(_("Sold liters do not match difference from starting and ending wight"))
                self.env['pos_route_config.route_config'].sudo().write([config])
            if session.state == 'closing_control':
                if not session.can_close_session:
                    raise ValidationError(_('The route configuration for this session must be closed first'))
        return True

    def _is_gaspar_conciliated(self):
        for session in self:
            # TODO no es necesario verificar si estan conciciliado si la unidad gaspar no está disponible 
            session.gaspar_orders_cons = True
            config = session.config_id
            if not config.is_gaspar_available:
                return
            orders = self.env['pos.order'].search([('session_id', '=', session.id)])
            refunds = session.order_ids.get_refunds()
            for order in orders:
                # TODO agregar permiso a la condición
                if order.pos_reference not in refunds.keys():
                    if order.total_lt > 0 and not order.gaspar_conciliated:
                        session.gaspar_orders_cons = False
                        return 

    def action_pos_session_closing_control_recalculate_stock(self):
        res = self.action_pos_session_validate()
        # self._recalculate_stock()
        return res

    def action_view_route_config(self):
        route_config = self.env['pos_route_config.route_config'].search([('session_id', '=', self.id)])
        return {
            'name': _('Route config'),
            'res_model': 'pos_route_config.route_config',
            'view_mode': 'form',
            'views': [
                (self.env.ref('pos_route_config.view_pos_route_config_route_config_form').id, 'form')
            ],
            'type': 'ir.actions.act_window',
            'res_id': route_config.id,
        } 

    def _recalculate_stock(self):
        for session in self:
            config = session.config_id
            if not config.is_gaspar_available:
                return
            location = session.config_id.picking_type_id.default_location_src_id
            total_lt = 0.0
            total_gaspar_lt = 0.0
            refunds = session.order_ids.get_refunds()
            for order in session.order_ids:
                if order.pos_reference not in refunds.keys():
                    total_lt += order.total_lt
                    total_gaspar_lt += order.total_lt_gas
            total = total_lt - total_gaspar_lt
            # if total > 0:
            uom = self.env['uom.uom'].search([('name', '=', 'LT'), ('active', '=', True)])
            # product_template = self.env['product.template'].search([('is_gas', '=', True), ('uom_id', '=', uom.id), ('company_id', '=', self.env.company.id), ('active', '=', True)])
            product_template = self.env['product.template'].search([('name', '=', 'Gas Licuado de Petróleo'), ('uom_id', '=', uom.id), ('company_id', '=', self.env.company.id), ('active', '=', True)])
            product = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)])
            self.env['stock.quant']._update_available_quantity(product, location, total)

    # def get_gaspar_data(self):
    #     params = {'serverName': self.env.company.g4s_server, 'references': []}
    #     orders = self.env['pos.order'].search([('session_id', '=', self.id)])
    #     for order in orders:
    #         params['references'].append(order.note)
    #     req = urllib.request.Request(url='https://localhost:44345/api/sale', data=json.dumps(params).encode(),
    #         headers={"Content-Type": "application/json"}, method='GET')
    #     res = json.loads(urllib.request.urlopen(req).read().decode())
    #     refs = {}
    #     for sale in res:
    #         refs[sale['ius_64']] = sale
    #     for order in orders:
    #         if order.note:
    #             if order.note in refs.keys():
    #                 order.hg = refs[order.note]['scheme']
    #                 order.total_lt_gas = refs[order.note]['total_volume']
    #     print(res)
                    
