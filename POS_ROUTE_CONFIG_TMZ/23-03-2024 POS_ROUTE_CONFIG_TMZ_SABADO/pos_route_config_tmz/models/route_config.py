from ast import If
from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
from pytz import timezone
from odoo.tools import float_round
import logging
_logger = logging.getLogger(__name__)


class RC_report(models.Model): 
    _name = 'pos_route_config_tmz.c_report'
    _description = 'reportes'

    name = fields.Char(string='Nombre ', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company)
    fecha_filtro = fields.Date(string='Fecha de configuración de ruta ')
    fecha_reporte = fields.Datetime(string='Fecha de creación ', readonly=True, default=lambda self: fields.datetime.now())#

    relacion_ids = fields.Many2many(comodel_name='pos_route_config_tmz.rd',  inverse_name='data_ids', string='Relacion')
    
    @api.model
    def create(self, vals):
        vals['name'] = 'Reporte de rutas de configuración: ' + vals['fecha_filtro']
        return super(RC_report, self).create(vals)



    
    def _get_time_zone(self):
        res_users_obj = self.env['res.users']
        userstz = res_users_obj.browse(self._uid).tz
        a = 0#ggg
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
        vals['name'] = 'Reporte de rutas de configuración: ' + vals['fecha_filtro']
        return super(RC_report, self).write(self, vals)
    
    
    @api.onchange('fecha_filtro')
    def _get_name(self): 
        for doc in self:
            if doc.fecha_filtro:

                init_date = doc.fecha_filtro
                out_date = doc.fecha_filtro
                time_zone = self._get_time_zone()

                 # --------------------------------------------------------- Fecha ---------------------------------------------------------

                fecha_entrada = init_date.strftime("%Y-%m-%d")
                fecha_salida = out_date.strftime("%Y-%m-%d")
                
                date_start = fecha_entrada + ' 00:00:00'
                date_end = fecha_salida + ' 23:59:59' # 17:00:00 hrs del servidor 23:59:59

                date_start_search = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S') + timedelta(hours=abs(time_zone))
                date_end_search = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S') + timedelta(hours=abs(time_zone))
                rec = self.env['pos_route_config.route_config'].search([('create_date', '>=', date_start_search), ('create_date', '<=', date_end_search), ("company_id.name", "=", doc.company_id.name)]) #search([('anno', '=', doc.fecha_filtro)]) 
                self.relacion_ids = [(5,0,0)]
                for res in rec:
                    line = {}
                    line['route_creation_date'] = res.create_date #fecha de creacion de la ruta
                    line['departure_date'] = res.departure_date
                    line['arrival_date'] = res.arrival_date
                    line['name'] = res.name
                    line['pos_config_id'] = res.pos_config_id
                    line['st_volume_meter'] = res.st_volume_meter
                    line['en_volume_meter'] = res.en_volume_meter
                    line['dif_volume_meter'] = res.dif_volume_meter
                    line['st_weight_aux'] = res.st_weight_aux
                    line['en_weight_aux'] = res.en_weight_aux
                    line['dif_weight'] = res.dif_weight
                    line['st_percent'] = res.st_percent
                    line['en_percent'] = res.en_percent
                    line['dif_percent'] = res.dif_percent
                    line['avg_sector'] = res.avg_sector 
                    line['hg_avg'] = res.hg_avg         
                    line['st_carburation'] = res.st_carburation
                    line['en_carburation'] = res.en_carburation
                    line['dif_carburation'] = res.dif_carburation
                    line['st_gauge'] = res.st_gauge
                    line['en_gauge'] = res.en_gauge
                    line['liters_receivable'] = res.liters_receivable   
                    line['refuel_liters'] = res.refuel_liters
                    line['state'] = res.state
                    for employee in res.employee_ids:
                        line['employee_ids'] = [(4, employee.id)]
                        #line['employee_ids'] = res.employee_ids b
                    line['x_studio_ayudante'] = res.x_studio_ayudante
                    line['justification'] = res.justification
                    self.relacion_ids = [(0,0,line)]



class reporte_s(models.Model): #este almacena los datos
    _name = 'pos_route_config_tmz.rd'
    _description = 'Almacen de datos'

    data_ids = fields.Many2one(comodel_name='pos_route_config_tmz.c_report', string='Variables', readonly=True)
    route_creation_date = fields.Datetime(string='Fecha de creación')
    departure_date = fields.Datetime(string='Fecha de salida')
    arrival_date = fields.Datetime(string='Fecha de llegada')
    name = fields.Char(string='Referencia de ruta', default='Nuevo')
    pos_config_id = fields.Many2one(comodel_name='pos.config', string='Punto de venta')
    st_volume_meter = fields.Float(string='Litrómetro inicial')
    en_volume_meter = fields.Float(string='Litrómetro final')
    dif_volume_meter = fields.Float(string='Diferencia de litrómetro')
    st_weight = fields.Float(string='Peso inicial')
    st_weight_aux = fields.Float(string='Peso inicial Aux')
    en_weight = fields.Float(string='Peso final')
    en_weight_aux = fields.Float(string='Peso final Aux')
    dif_weight = fields.Float(string='Diferencia de peso') 
    st_percent = fields.Float(string='Porcentaje inicial')
    en_percent = fields.Float(string='Porcentaje final')
    dif_percent = fields.Float(string='Diferencia de porcentaje')
    avg_sector = fields.Float(string='Promedio sector')#Promedio sector
    hg_avg = fields.Float(string='Promedio general')#Promedio general
    st_carburation = fields.Integer(string="Carburación inicial")
    en_carburation = fields.Integer(string="Carburación final")   
    dif_carburation = fields.Integer(string='Diferencia de carburación')
    st_gauge = fields.Integer(string='Rotogauge inicial')
    en_gauge = fields.Integer(string='Rotogauge final')
    refuel_liters = fields.Float(string="Litros para recargar")
    liters_receivable = fields.Float(string="Litros por cobrar")
    state = fields.Selection(string='Estatus',
        selection=[('new', 'Nuevo'), #izq: lo que se verá en el reporte (excel), der: lo que se mostrará en la vista al jalar los datos
                   ('start', 'Configuración de Ruta'), 
                   ('sale', 'Ventas'), 
                   ('reception', 'Recepción de rutas'), 
                   ('concil', 'Conciliación de venta'), 
                   ('finish', 'Cierre de caja')])
    employee_ids = fields.Many2many(comodel_name='hr.employee', string='Empleado')
    x_studio_ayudante = fields.Many2one('hr.employee', string='Ayudante') 
    justification = fields.Text(string='Justificación')
