# -*- coding: utf-8 -*-

from ast import If
from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
from pytz import timezone
from odoo.tools import float_round
import logging
_logger = logging.getLogger(__name__)


class Create_Rep(models.Model): 
    _name = 'r_descuento_integrado.cr'
    _description = 'reportes'

    name = fields.Char(string='Nombre ', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company)
    
    fecha_inicio = fields.Date(string='Fecha inicial')
    fecha_final = fields.Date(string='Fecha final')
    fecha_reporte = fields.Datetime(string='Fecha de creación ', readonly=True, default=lambda self: fields.datetime.now())#

    relacion_ids = fields.Many2many(comodel_name='r_descuento_integrado.rd',  inverse_name='data_ids', string='Relacion')
    
    @api.model
    def create(self, vals):
        vals['name'] = 'Reporte de descuento integrado: ' + vals['fecha_inicio'] + ' - ' + vals['fecha_final']
        return super(Create_Rep, self).create(vals)
    

    # def write(self, vals):
    #     if 'fecha_inicio' in vals or 'fecha_final' in vals:
    #         vals['name'] = 'Reporte de descuento integrado: ' + vals.get('fecha_inicio', self.fecha_inicio) + ' - ' + vals.get('fecha_final', self.fecha_final)
    #     return super(Create_Rep, self).write(vals)





    
    def _get_time_zone(self):
        res_users_obj = self.env['res.users']
        userstz = res_users_obj.browse(self._uid).tz
        a = 0
        if userstz:
            hours = timezone(userstz)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            now = datetime.now()
            loc_dt = hours.localize(datetime(now.year, now.month, now.day,
                                             now.hour, now.minute, now.second))
            timezone_loc = (loc_dt.strftime(fmt))
            diff_timezone_original = timezone_loc[-5:-2]
            timezone_original = int(diff_timezone_original)
            s = str(datetime.now(timezone(userstz)))
            s = s[-6:-3]
            timezone_present = int(s)*-1
            a = timezone_original + ((
                timezone_present + timezone_original)*-1)
        return a
    
    def write(self, vals):
        vals['name'] = 'Reporte de descuento integrado: ' + vals['fecha_inicio'] + ' - ' + vals['fecha_final']
        return super(Create_Rep, self).write(self, vals)
    
    
    @api.onchange('fecha_inicio', 'fecha_final')
    def _get_name(self): 
        for doc in self:
            if doc.fecha_inicio and doc.fecha_final:

                init_date = doc.fecha_inicio
                out_date = doc.fecha_final
                time_zone = self._get_time_zone()

                 # --------------------------------------------------------- Fecha ---------------------------------------------------------

                fecha_entrada = init_date.strftime("%Y-%m-%d")
                fecha_salida = out_date.strftime("%Y-%m-%d")
                
                date_start = fecha_entrada + ' 00:00:00'
                date_end = fecha_salida + ' 23:59:59' # 17:00:00 hrs del servidor 23:59:59

                date_start_search = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S') + timedelta(hours=abs(time_zone))
                date_end_search = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S') + timedelta(hours=abs(time_zone))
                
                
                # notas = self.env['account.move'].search(["|"('invoice_date', '>=',  doc.fecha_inicio), ('invoice_date', '<=', doc.fecha_final), ('move_type', '=', 'out_invoice'), ("total_cash_discount", ">", 0), ("edi_state","=","sent"), ("edi_state","=","to_cancel")])
                notas = self.env['account.move'].search(["&","&",["invoice_date",">=",doc.fecha_inicio],["invoice_date","<=",doc.fecha_final],"|","|","|",["move_type","=","out_invoice"],["total_cash_discount",">",0],["edi_state","=","sent"],["edi_state","=","to_cancel"]])

                self.relacion_ids = [(5,0,0)]
                for res in notas:
                    line = {}
                    line['name'] = res.name
                    line['partner_id'] = res.invoice_partner_display_name
                    line['invoice_date'] = res.invoice_date
                    # line['total_cash_discount'] = res.total_cash_discount
                    self.relacion_ids = [(0,0,line)]


class reporte_save(models.Model): #este almacena los dato
    _name = 'r_descuento_integrado.rd'
    _description = 'Almacen de datos'

    data_ids = fields.Many2one(comodel_name='r_descuento_integrado.cr', string='Variables', readonly=True)

    name = fields.Char(string='Nombre')
    partner_id = fields.Char(string='Cliente')
    invoice_date = fields.Date(string='Fecha de la factura')
    # total_cash_discount = fields.Monetary(string='Descuento')


    

