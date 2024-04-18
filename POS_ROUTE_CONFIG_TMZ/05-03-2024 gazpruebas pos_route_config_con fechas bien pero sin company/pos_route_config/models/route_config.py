from ast import If
from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
from pytz import timezone
from odoo.tools import float_round
import logging
_logger = logging.getLogger(__name__)

class RouteConfiguration(models.Model):
    _name = 'pos_route_config.route_config'
    _description = 'Route configuration'
    _check_company_auto = True
    _order = 'id desc'

    anno = fields.Date(string='Año', default=fields.Date.today())
    #fecha_filtro = fields.Date(string='Fecha de configuración de rutaR: ', default=fields.Date.today()) #AGREGADO K
    #fecha_reporte = fields.Date(string='Fecha  reporteR: ', default=fields.Date.today())

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company)
    date = fields.Date(string='Date', default=fields.Date.today())
    departure_date = fields.Datetime(string='Departure', default=fields.Datetime.now())
    departure_approved_by_uid = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user)
    arrival_date = fields.Datetime(string='Arrival')
    arrival_approved_by_uid = fields.Many2one(comodel_name='res.users')
    name = fields.Char(string='Route Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    pos_config_id = fields.Many2one(comodel_name='pos.config', string='Point of sale')
    session_id = fields.Many2one(comodel_name='pos.session', string="Point of sale session")
    st_weight = fields.Float(string='Starting Weight')

    st_weight_aux = fields.Float(string='Starting Weight Aux')

    st_volume_meter = fields.Float(string='Starting Volume')
    st_percent = fields.Float(string='Starting Percentage')
    st_gauge = fields.Integer(string='Starting Rotogauge')
    # TODO quitar para islasf
    st_carburation = fields.Integer(string="Starting Carburation", default=90)
    en_weight = fields.Float(string='Ending Weight')
    en_weight_aux = fields.Float(string='Ending Weight Aux')
    en_volume_meter = fields.Float(string='Ending Volume')
    en_percent = fields.Float(string='Ending Percentage')
    en_gauge = fields.Integer(string='Ending Rotogauge')
    # TODO Quitar para islas
    en_carburation = fields.Integer(string="Ending Carburation", default=90)

    dif_weight = fields.Float(string='Weight Difference', compute='_compute_weight_dif', store=True) 
    dif_volume_meter = fields.Float(string='Volume Difference', compute='_compute_volume_dif', store=True)
    dif_percent = fields.Float(string='Percentage Difference', compute='_compute_percent_dif', store=True)
    dif_gauge = fields.Integer(string='Rotogauge  Difference', compute='_compute_gauge_dif')
    dif_carburation = fields.Integer(string='Carburation Difference', compute='_compute_carb_dif', store=True)

    dif_percent_volume = fields.Float(string='Percent Difference (L)', compute='_compute_percent_vol_dif')
    dif_weight_volume = fields.Float(string='Weight Difference (L)', compute='_compute_weight_vol_dif')
    rebombeo = fields.Boolean(string='Rebombeo', compute='_compute_rebombeo')

    refuel_liters = fields.Float(string="Liters to refuel")

    dif_kilos = fields.Float(string='Dif. kilos', compute='_compute_kilos_dif')

    state = fields.Selection(string='Status', default='new',
        selection=[('new', 'New'), 
                   ('start', 'Route Configuration'), 
                   ('sale', 'Sales'), 
                   ('reception', 'Route Reception'), 
                   ('concil', 'Sale Conciliation'), 
                   ('finish', 'Cash Box Closed')])

    refuel_state = fields.Selection(string='Refuel State', default="unpaid",
        selection=[('unpaid', 'Unpaid'), ('paid', 'Paid')])

    crm_team_id = fields.Many2one(comodel_name='crm.team', string='Sales team')
    employee_ids = fields.Many2many(comodel_name='hr.employee', string='Employee')
    can_edit_form = fields.Boolean(string='Can edit form?', compute='_can_edit_form')
    can_edit_start_volume = fields.Boolean(string='Can edit starting volume?', default= lambda self: self._can_edit_start_volume(), compute='_compute_can_edit_start_volume')

    can_writing_weight = fields.Boolean(string='Can writing weight?', default=True , compute='_compute_can_writing_weight') 
    can_edit_st_weight = fields.Boolean(string='Can edit starting weight?', compute='_can_edit_st_weight')
    can_edit_en_weight = fields.Boolean(string='Can edit ending weight?', compute='_can_edit_en_weight')

    # can_edit_st_weight = fields.Boolean(string='Can edit statrting weight', default= lambda self: self._can_edit_st_weight(), compute='_compute_can_edit_st_weight')
    # can_edit_en_weight = fields.Boolean(string='Can edit ending weight', default= lambda self: self._can_edit_en_weight(), compute='_compute_can_edit_en_weight')

    st_tank_10_kg = fields.Integer(string="Starting 10 Kg tank", default=0)
    st_tank_20_kg = fields.Integer(string="Starting 20 Kg tank", default=0)
    st_tank_27_kg = fields.Integer(string="Starting 27 Kg tank", default=0)
    st_tank_30_kg = fields.Integer(string="Starting 30 Kg tank", default=0)
    st_tank_45_kg = fields.Integer(string="Starting 45 Kg tank", default=0)
    st_tank_bulk = fields.Float(string="Starting Bulk")
    en_tank_10_kg = fields.Integer(string="Ending 10 Kg tank", default=0)
    en_tank_20_kg = fields.Integer(string="Ending 20 Kg tank", default=0)
    en_tank_27_kg = fields.Integer(string="Ending 27 Kg tank", default=0)
    en_tank_30_kg = fields.Integer(string="Ending 30 Kg tank", default=0)
    en_tank_45_kg = fields.Integer(string="Ending 45 Kg tank", default=0)
    en_tank_bulk = fields.Float(string="Ending Bulk")

    x_studio_tipo_almacn = fields.Selection(string='Tipo Almacén', compute="_get_location_type",
        selection=[('Almacén', 'Almacén'), 
                   ('Portátil', 'Portátil'), 
                   ('Autotanque', 'Autotanque'), 
                   ('Carburación', 'Carburación')])

    justification = fields.Text(string='Justification')
    is_justification_nedeed = fields.Boolean(string='Is justification needed?', default=False)
    st_volume_meter_default = fields.Float(string='Starting Volume Default')

    percent_justification = fields.Text(string="Percentage justification", required=True)
    percent_just_flag = fields.Boolean(string='Is percent justification required?', default=False)    

    @api.onchange('st_weight_aux')
    def bloq_edit_st_weight(self):
        if self.st_weight_aux != 0.00:
            self.st_weight = self.st_weight_aux
            self.can_edit_st_weight = False
        elif self.st_weight_aux == 0.00 and self.state == 'new':
            self.can_edit_st_weight = True

    @api.onchange('en_weight_aux')
    def bloq_edit_en_weight(self):
        if self.en_weight_aux != 0.00:
            self.en_weight = self.en_weight_aux
            self.can_edit_en_weight = False
        elif self.en_weight_aux == 0.00 and self.state == 'sale':
            self.can_edit_en_weight = True

    @api.onchange('en_percent')
    def _en_percent_on_change(self):
        for route in self:
            route.percent_just_flag = False
            if route.st_percent < route.en_percent:
                route.percent_just_flag = True

    @api.depends('can_edit_form', 'state')
    def _can_edit_st_weight(self):
            if self.can_edit_form:
                self.can_edit_st_weight = self.can_edit_form
            else:
                if self.st_weight_aux != 0.00:
                    self.st_weight = self.st_weight_aux
                    self.can_edit_st_weight = False
                elif self.st_weight_aux == 0.00 and self.state == 'new':
                    self.can_edit_st_weight = True
                elif self.st_weight_aux == 0.00 and self.state != 'new':
                    self.can_edit_st_weight = False

    @api.depends('can_edit_form', 'state')
    def _can_edit_en_weight(self):
            if self.can_edit_form:
                self.can_edit_en_weight = self.can_edit_form
            else:
                if self.en_weight_aux != 0.00:
                    self.en_weight = self.st_weight_aux
                    self.can_edit_en_weight = False
                elif self.en_weight_aux == 0.00 and self.state == 'sale':
                    self.can_edit_en_weight = True
                elif self.en_weight_aux == 0.00 and self.state != 'sale':
                    self.can_edit_en_weight = False



    # @api.depends('can_edit_form', 'state')
    # def _can_edit_st_weight(self):
    #     if self.env.company.use_weight_scale:
    #         return not self.env.company.use_weight_scale
    #     elif not self.state:
    #         return True
    #     elif self.state != 'new' and self.env.user.has_group('pos_route_config.group_route_config_edit'):
    #         return self.env.user.has_group('pos_route_config.group_route_config_edit')
    #     return False

    # @api.depends('state') 
    @api.depends('can_edit_form')
    def _can_writing_weight(self):
        if self.state:
            if self.env.company.use_weight_writing:
                self.can_writing_weight = self.env.user.has_group('pos_route_config.group_route_config_writing_weight')
            else:
                self.can_writing_weight = False

    def _compute_can_writing_weight(self):   
        self._can_writing_weight() 

    # @api.depends('session_id','liters_receivable')
    def _compute_refuel_liters(self):
        if self.pos_config_id.is_gaspar_available:
            # _logger.info(self.pos_config_id.is_gaspar_available)
            # if len(self.servicios_ids) >= 1:
            total_lt = sum(line.volumen for line in self.servicios_ids) 
            # _logger.info(total_lt * (self.avg_sector / 100))
            self.refuel_liters = total_lt * (self.avg_sector / 100)
        else:
            if not self.pos_config_id.eficiencia:
                raise UserError('Es necesario configurar la eficiencia para el punto de venta seleccionado')
            # _logger.info(self.liters_receivable * (self.pos_config_id.eficiencia / 100))
            self.refuel_liters = self.liters_receivable * (self.pos_config_id.eficiencia / 100)

        # for route in self:
        #     _logger.info(route.session_id.id)
        #     orders = self.env['pos.order'].search([('session_id', '=', route.session_id.id)])
        #     route.refuel_liters = 0
        #     if orders:
        #         for order in orders:
        #             route.refuel_liters += order.total_lt_gas

    # @api.depends('can_edit_form')
    def _compute_can_edit_st_weight(self):
        self.can_edit_st_weight = self._can_edit_st_weight()

    # @api.depends('can_edit_form', 'state')
    # def _can_edit_en_weight(self):
    #     if not self.state:
    #         return True
    #     if self.env.company.use_weight_scale:
    #         return not self.env.company.use_weight_scale
    #     if self.state == 'sale':
    #         return True
    #     return self.env.user.has_group('pos_route_config.group_route_config_edit')

    def _compute_can_edit_en_weight(self):
        self.can_edit_en_weight = self._can_edit_en_weight()

    @api.depends('pos_config_id')
    def _get_location_type(self):
        for conf in self:
            conf.x_studio_tipo_almacn = conf.pos_config_id.picking_type_id.default_location_src_id.x_studio_tipo_almacn
    
    @api.depends('st_weight', 'en_weight')
    def _compute_weight_dif(self):
        self.dif_weight = self.st_weight - self.en_weight

    @api.depends('st_weight', 'en_weight')
    def _compute_weight_vol_dif(self):
        self.dif_weight_volume = (self.st_weight - self.en_weight) / 0.54

    @api.depends('dif_volume_meter', 'dif_percent_volume')
    def _compute_rebombeo(self):
        self.rebombeo = False
        if self.state in ('reception', 'concil', 'finish'):
            self.rebombeo = self.dif_volume_meter < self.dif_percent_volume

    @api.depends('st_volume_meter', 'en_volume_meter')
    def _compute_volume_dif(self):
        self.dif_volume_meter = float_round((self.en_volume_meter - self.st_volume_meter), precision_digits=2, precision_rounding=None)

    @api.depends('st_percent', 'en_percent')
    def _compute_percent_dif(self):
        self.dif_percent = self.st_percent - self.en_percent
    
    @api.depends('st_percent', 'en_percent')
    def _compute_percent_vol_dif(self):
        max_capacity = 0.0
        limits = self.pos_config_id.picking_type_id.default_location_src_id.limit_ids
        if limits:
            max_capacity = limits[0].qty
        self.dif_percent_volume = (self.st_percent - self.en_percent) * max_capacity / 100

    @api.depends('st_gauge', 'en_gauge')
    def _compute_gauge_dif(self):
        self.dif_gauge = self.st_gauge - self.en_gauge

    @api.depends('st_carburation', 'en_carburation')
    def _compute_carb_dif(self):
        self.dif_carburation = self.st_carburation - self.en_carburation

    @api.depends('st_tank_10_kg', 'st_tank_20_kg', 'st_tank_27_kg', 'st_tank_30_kg', 'st_tank_45_kg', 'st_tank_bulk',
                 'en_tank_10_kg', 'en_tank_20_kg', 'en_tank_27_kg', 'en_tank_30_kg', 'en_tank_45_kg', 'en_tank_bulk')
    def _compute_kilos_dif(self):
        st_total_kilos = 0.00
        en_total_kilos = 0.00

        st_total_kilos += (self.st_tank_10_kg * 10)
        st_total_kilos += (self.st_tank_20_kg * 20)
        st_total_kilos += (self.st_tank_27_kg * 27)
        st_total_kilos += (self.st_tank_30_kg * 30)
        st_total_kilos += (self.st_tank_45_kg * 45)
        st_total_kilos += self.st_tank_bulk 

        en_total_kilos += (self.en_tank_10_kg * 10)
        en_total_kilos += (self.en_tank_20_kg * 20)
        en_total_kilos += (self.en_tank_27_kg * 27)
        en_total_kilos += (self.en_tank_30_kg * 30)
        en_total_kilos += (self.en_tank_45_kg * 45)
        en_total_kilos += self.en_tank_bulk 


        self.dif_kilos = float_round((st_total_kilos - en_total_kilos), precision_digits=2, precision_rounding=None)
    
    def _can_edit_form(self):
        if self.env.company.use_weight_scale:
            self.can_edit_form = self.env.user.has_group('pos_route_config.group_route_config_edit')
        print(self.can_edit_form)

    def _can_edit_start_volume(self):
        return self.env.user.has_group('pos_route_config.group_route_config_edit_start_volume')
    
    def _compute_can_edit_start_volume(self):
        self.can_edit_start_volume = self._can_edit_start_volume()


    @api.onchange('st_volume_meter')
    def st_volume_meter_on_change(self):
        if self.st_volume_meter != self.st_volume_meter_default:
            self.is_justification_nedeed = True
        else:
            self.is_justification_nedeed = False

    @api.onchange('pos_config_id')
    def pos_config_on_change(self):
        if self.pos_config_id:
            self.x_studio_tipo_almacn = self.pos_config_id.picking_type_id.default_location_src_id.x_studio_tipo_almacn
            route_config = self.env['pos_route_config.route_config'].search([('pos_config_id', '=', self.pos_config_id.id), ('state', '=', 'finish')], order='id desc', limit=1)
            self.is_justification_nedeed = False
            if route_config:
                self.st_volume_meter = route_config.en_volume_meter
                self.st_volume_meter_default = route_config.en_volume_meter
                self.employee_ids = route_config.employee_ids
            else:
                self.st_volume_meter = 0
                self.st_volume_meter_default = 0

    @api.model
    def create(self, vals):
        _route_conf = self.env['pos_route_config.route_config'].search([('pos_config_id', '=', vals['pos_config_id']), ('state', '!=', 'finish')])
        pos_session = self.env['pos.session'].search([('config_id','=', vals['pos_config_id']), ('state','!=','closed')])
        if pos_session or _route_conf:
            raise ValidationError(_("Can't start a new route until last route or POS session have been closed"))
        pos_config = self.env['pos.config'].search([('id', '=', vals['pos_config_id'])])
        if pos_config.can_start_session:
            raise ValidationError(_('Last route configuration must be closed before opening a new one'))
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('route_config.sequence') or _('New')
        self.send_meter_change_mail(vals)
        pos_config.can_start_session = True
        pos_config.employee_ids = vals['employee_ids']
        self.env['pos.config'].write([pos_config])
        vals['state'] = 'start'
        vals['justification'] = False
        vals['is_justification_nedeed'] = False
        if self.env.company.use_weight_scale:
            vals['st_weight'] = vals['st_weight_aux']
        if not self._can_edit_start_volume():
            vals['st_volume_meter'] = vals['st_volume_meter_default']
        vals.pop('justification', None)
        route_conf = super(RouteConfiguration, self).create(vals)
        route_conf_hist = self._transform_route_to_hist(route_conf)
        self.env['pos_route_config.route_config_history'].create([route_conf_hist])

        return route_conf

    def send_meter_change_mail(self, vals):
        if 'is_justification_nedeed' in vals.keys():
            if vals['is_justification_nedeed']:
                if not vals['justification']:
                    raise UserError(_('Due to a volume meter change, a justification is nedeed'))
                # supervisor_id = self.env['ir.config_parameter'].get_param('pos_route_config.supervisor')
                supervisor = self.env.company.supervisor_user_id
                _justification = {
                    'justification' : vals['justification'],
                    'st_volume_meter_default' : vals['st_volume_meter_default'],
                    'st_volume_meter' : vals['st_volume_meter'],
                    'supervisor_mail' : supervisor.email_formatted,
                    'unit' : vals['name']
                }
                id_justification = self.env['pos_route_config.justification'].create([_justification])
                mail_template_id = self.env.ref('pos_route_config.route_config_mail_template').id
                self.env['mail.template'].browse(mail_template_id).send_mail(id_justification.id, force_send=True)


    def write(self, vals):
        if isinstance(vals, dict):
            for route in self:
                route_conf_hist = self._transform_route_to_hist(route)
                if (not self.can_edit_en_weight and 'en_weight_aux' in vals):
                    vals['en_weight'] = vals['en_weight_aux']
                # if (self.can_edit_form and not self.can_edit_st_weight and 'st_weight_aux' in vals):
                if (self.can_edit_form and not self.can_edit_st_weight and 'st_weight' in vals):
                     vals['st_weight'] = vals['st_weight_aux']
                for key in vals.keys():
                    if not key == 'servicios_ids':
                        route_conf_hist[key] = vals[key] 
                self.env['pos_route_config.route_config_history'].create([route_conf_hist])
            if 'is_justification_nedeed' in vals:
                vals['st_volume_meter_default'] = self.st_volume_meter
                vals['name'] = self.name
                self.send_meter_change_mail(vals)
            vals['is_justification_nedeed'] = False
            vals.pop('justification', None)
            return super(RouteConfiguration, self).write(vals)


    def finish_route_config(self):
        # pos_config = self.env['pos.config'].search(['id', '=', vals['id']])
        for route_conf in self:
            if not route_conf.x_studio_tipo_almacn == 'Portátil':
                if route_conf.st_percent < route_conf.en_percent and not self.percent_justification:
                    raise ValidationError(_("Starting percentage must be greater than Ending Percentage or add a justification"))
                if route_conf.st_weight < route_conf.en_weight:
                    raise ValidationError(_("Starting Weight must be greater than Ending Weight"))
                if route_conf.st_volume_meter > route_conf.en_volume_meter:
                    raise ValidationError(_("Starting Volume must be lower than Ending volume"))
            else:
                if route_conf.st_tank_10_kg < route_conf.en_tank_10_kg:
                    raise UserError(_("Starting 10 kg tank cannot be lower than Ending 10 kg tank"))
                if route_conf.st_tank_20_kg < route_conf.en_tank_20_kg:
                    raise UserError(_("Starting 20 kg tank cannot be lower than Ending 20 kg tank"))
                if route_conf.st_tank_27_kg < route_conf.en_tank_27_kg:
                    raise UserError(_("Starting 27 kg tank cannot be lower than Ending 27 kg tank"))
                if route_conf.st_tank_30_kg < route_conf.en_tank_30_kg:
                    raise UserError(_("Starting 30 kg tank cannot be lower than Ending 30 kg tank"))
                if route_conf.st_tank_45_kg < route_conf.en_tank_45_kg:
                    raise UserError(_("Starting 45 kg tank cannot be lower than Ending 45 kg tank"))
                if route_conf.st_tank_bulk < route_conf.en_tank_bulk:
                    raise UserError(_("Starting bulk cannot be lower than Ending bulk"))
            session = route_conf.session_id #self.env['pos.session'].search([('config_id', '=', route_conf.pos_config_id.id), ('state', '=', 'opened')])
            pos_config = self.env['pos.config'].search([('id', '=', route_conf.pos_config_id.id)])
            if not session:
                raise ValidationError(_("Can't finish this route until a new POS session has been created"))
            session.can_close_session = True
            session.state = 'closing_control'
            session.stop_at = fields.Datetime.now()
            self.env['pos.session'].write([session])
            route_conf.state = 'reception'
            route_conf['arrival_approved_by_uid'] = self.env.user.id
            if not self.arrival_date:
                self.arrival_date = fields.Datetime.now()
            pos_config.can_start_session = False
            self.env['pos.session'].write([pos_config])
            self.env['pos_route_config.route_config'].write([route_conf])
        return True

    @api.constrains('st_percent')
    def _check_st_percent(self):
        for route_config in self:
            if route_config.st_percent < 0.0 or route_config.st_percent > 100.0:
                raise ValidationError(_("Starting Percentage can't be lower than 0 or higher than 100"))
        return True

    @api.constrains('en_percent')
    def _check_en_percent(self):
        for route_config in self:
            if route_config.en_percent < 0.0 or route_config.en_percent > 100.0:
                raise ValidationError(_("Ending Percentage can't be lower than 0 or higher than 100"))
        return True

    @api.constrains('st_carburation')
    def _check_st_carburation(self):
        for route_config in self:
            if route_config.st_carburation < 0 or route_config.st_carburation > 100:
                raise ValidationError(_("Starting Carburation can't be lower than 0 or higher than 100"))
        return True
    
    @api.constrains('en_carburation')
    def _check_en_carburation(self):
        for route_config in self:
            if route_config.en_carburation < 0 or route_config.en_carburation > 100:
                raise ValidationError(_("Ending Carburation can't be lower than 0 or higher than 100"))
        return True
    
    def action_view_route_history(self):
        return {
            'name': _('History'),
            'res_model': 'pos_route_config.route_config_history',
            'view_mode': 'form',
            'views': [
                (self.env.ref('pos_route_config.pos_route_config_route_config_history_view_tree').id, 'tree')
            ],
            'type': 'ir.actions.act_window',
            'domain': [('route_config_id', '=', self.id)],
        } 

    def action_view_session(self):
        return {
            'name': _('Session'),
            'res_model': 'pos.session',
            'view_mode': 'form',
            'views': [
                (self.env.ref('point_of_sale.view_pos_session_form').id, 'form')
            ],
            'type': 'ir.actions.act_window',
            'res_id': self.session_id.id,
        } 

    def revert_route_state(self):
        for route in self:
            session = route.session_id
            if not session:
                session = self.env['pos.session'].search([('state', '=', 'closing_control'), ('config_id', '=', route.pos_config_id.id)])
                if not session:
                    raise UserError(_("This point of sales has no session to recover"))         
            route.state = 'sale'      
            session.can_close_session = False
            session.state = 'opened'
            self.env['pos.session'].write([session])
            route.pos_config_id.can_start_session = True
            self.env['pos.config'].write([route.pos_config_id])

    def _transform_route_to_hist(self, route):
        route_conf_hist = {
                'route_config_id': route.id,
                'user_id': self.env.user.id,
                'state': route.state,
                'session_id': route.session_id.id,
                'refuel_state': route.refuel_state,
                'departure_date': route.departure_date,
                'departure_approved_by_uid': route.departure_approved_by_uid.id,
                'arrival_date': route.arrival_date,
                'arrival_approved_by_uid': route.arrival_approved_by_uid.id,
                'x_studio_tipo_almacn': route.x_studio_tipo_almacn,
                'st_weight': route.st_weight,
                'st_weight_aux': route.st_weight_aux, 
                'st_volume_meter': route.st_volume_meter, 
                'st_percent': route.st_percent, 
                'st_gauge': route.st_gauge, 
                'st_carburation': route.st_carburation, 
                'en_weight': route.en_weight, 
                'en_weight_aux': route.en_weight_aux, 
                'en_volume_meter': route.en_volume_meter,
                'en_percent': route.en_percent, 
                'en_gauge': route.en_gauge, 
                'en_carburation': route.en_carburation,
                'st_tank_10_kg': route.st_tank_10_kg,
                'st_tank_20_kg': route.st_tank_20_kg,
                'st_tank_27_kg': route.st_tank_27_kg,
                'st_tank_30_kg': route.st_tank_30_kg,
                'st_tank_45_kg': route.st_tank_45_kg,
                'st_tank_bulk': route.st_tank_bulk,
                'en_tank_10_kg': route.en_tank_10_kg,
                'en_tank_10_kg': route.en_tank_20_kg,
                'en_tank_10_kg': route.en_tank_27_kg,
                'en_tank_10_kg': route.en_tank_30_kg,
                'en_tank_10_kg': route.en_tank_45_kg,
                'en_tank_bulk': route.en_tank_bulk,
                'percent_justification': route.percent_justification,
                'percent_just_flag': route.percent_just_flag,
                'x_studio_ayudante': route.x_studio_ayudante.id,
                'employee_ids': route.employee_ids
                }
        return route_conf_hist


class RouteConfigurationHistory(models.Model):
    _name = 'pos_route_config.route_config_history'
    _description = 'Route Configuration History'

    route_config_id = fields.Many2one(string='Route configuration', comodel_name='pos_route_config.route_config')
    user_id = fields.Many2one(comodel_name='res.users', string='Modified by')
    date = fields.Date(string='Date', default=fields.Date.today())
    modified_date = fields.Datetime(string='Modified date', default=fields.Datetime.now())
    session_id = fields.Many2one(comodel_name='pos.session', string="Point of sale session")

    departure_date = fields.Datetime(string='Departure')
    departure_approved_by_uid = fields.Many2one(comodel_name='res.users')
    arrival_date = fields.Datetime(string='Arrival')
    arrival_approved_by_uid = fields.Many2one(comodel_name='res.users')
    
    can_edit_st_weight = fields.Boolean(string='Can edit starting weight?') 
    st_weight = fields.Float(string='Starting Weight')
    st_weight_aux = fields.Float(string='Starting Weight Aux')
    st_volume_meter = fields.Float(string='Starting Volume')
    st_percent = fields.Float(string='Starting Percentage')
    st_gauge = fields.Integer(string='Starting Rotogauge')
    st_carburation = fields.Integer(string="Starting Carburation")
    can_edit_en_weight = fields.Boolean(string='Can edit ending weight?') 
    en_weight = fields.Float(string='Ending Weight')
    en_weight_aux = fields.Float(string='Ending Weight Aux')
    en_volume_meter = fields.Float(string='Ending Volume')
    en_percent = fields.Float(string='Ending Percentage')
    en_gauge = fields.Integer(string='Ending Rotogauge')
    en_carburation = fields.Integer(string="Ending Carburation")   

    dif_weight = fields.Float(string='Weight Difference') 
    dif_volume_meter = fields.Float(string='Volume Difference')
    dif_percent = fields.Float(string='Percentage Difference')
    dif_gauge = fields.Integer(string='Rotogauge  Difference')
    dif_carburation = fields.Integer(string='Carburation Difference')
    dif_kilos = fields.Float(string='Kilograms Difference')

    state = fields.Selection(string='Status', default='new',
        selection=[('new', 'New'), ('start', 'Route Configuration'), ('sale', 'Sales'), ('reception', 'Route Reception'), ('concil', 'Sale Conciliation'), ('finish', 'Cash Box Closed')]) 

    refuel_state = fields.Selection(string='Refuel State', default="unpaid",
        selection=[('unpaid', 'Unpaid'), ('paid', 'Paid')])
    
    x_studio_tipo_almacn = fields.Selection(string='Tipo Almacén', 
        selection=[('Almacén', 'Almacén'), 
                   ('Portátil', 'Portátil'), 
                   ('Autotanque', 'Autotanque'), 
                   ('Carburación', 'Carburación')])    

    st_tank_10_kg = fields.Integer(string="Starting 10 Kg tank")
    st_tank_20_kg = fields.Integer(string="Starting 20 Kg tank")
    st_tank_27_kg = fields.Integer(string="Starting 27 Kg tank")
    st_tank_30_kg = fields.Integer(string="Starting 30 Kg tank")
    st_tank_45_kg = fields.Integer(string="Starting 45 Kg tank")
    st_tank_bulk = fields.Float(string="Starting Bulk")
    en_tank_10_kg = fields.Integer(string="Ending 10 Kg tank")
    en_tank_20_kg = fields.Integer(string="Ending 20 Kg tank")
    en_tank_27_kg = fields.Integer(string="Ending 27 Kg tank")
    en_tank_30_kg = fields.Integer(string="Ending 30 Kg tank")
    en_tank_45_kg = fields.Integer(string="Ending 45 Kg tank")
    en_tank_bulk = fields.Float(string="Ending Bulk")

    percent_justification = fields.Text(string="Percentage justification")
    percent_just_flag = fields.Boolean(string='Is percent justification required?', default=False)

    x_studio_ayudante = fields.Many2one('hr.employee', string='Ayudante')
    employee_ids = fields.Many2many(comodel_name='hr.employee', string='Employee')

    @api.model
    def create(self, vals):
        vals.pop('is_justification_nedeed', None)
        vals.pop('justification', None)
        rch = super(RouteConfigurationHistory, self).create(vals)
        return rch
    
    
from odoo import api, fields, models


class VolumeMeterJustification(models.Model):
    _name = 'pos_route_config.justification'
    _description = 'Volume meter change justification'

    justification = fields.Text(string='Justification')
    st_volume_meter_default = fields.Integer(string='Original value')
    st_volume_meter = fields.Integer(string='New value')
    supervisor_mail = fields.Char(string='Supervisor mail')
    unit = fields.Char(string='Unit')
    

class RouteConfigReport(models.AbstractModel):
    _name = 'report.pos_route_config.route_config_report'
    _description = 'Route Configuration Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('pos_route_config.route_config_report')
        return {
            'doc_ids' : docids,
            'doc_model' : self.env['pos_route_config.route_config'],
            'docs' : self.env['pos_route_config.route_config'].browse(docids)
        }


############################################################################################
class RC_report(models.Model): 
    _name = 'pos_route_config.create_report'
    _description = 'reportes'

    name = fields.Char(string='Nombre: ', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company)
    fecha_filtro = fields.Date(string='Fecha de configuración de ruta: ')
    fecha_reporte = fields.Datetime(string='Fecha de creación del reporte: ', readonly=True, default=lambda self: fields.datetime.now())

    relacion_ids = fields.Many2many(comodel_name='pos_route_config.report_data',  inverse_name='data_ids', string='Relacion')
    
    @api.model
    def create(self, vals):
        vals['name'] = 'Reporte de rutas de configuración: ' + vals['fecha_filtro']
        return super(RC_report, self).create(vals)

    
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
                date_end = fecha_salida + ' 23:59:59'

                date_start_search = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S') + timedelta(hours=abs(time_zone))
                date_end_search = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S') + timedelta(hours=abs(time_zone))
                rec = self.env['pos_route_config.route_config'].search([('create_date', '>=', date_start_search), ('create_date', '<=', date_end_search), ("company_id.name", "=", doc.company_id.name)]) #search([('anno', '=', doc.fecha_filtro)]) 
                self.relacion_ids = [(5,0,0)]
                for res in rec:
                    line = {}
                    #line['date'] = res.date
                    line['departure_date'] = res.departure_date
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
                        #line['employee_ids'] = res.employee_ids
                    line['x_studio_ayudante'] = res.x_studio_ayudante
                    line['justification'] = res.justification
                    self.relacion_ids = [(0,0,line)]



class reporte_s(models.Model): #esta almacena los datos
    _name = 'pos_route_config.report_data'
    _description = 'Almacen de datos'

    data_ids = fields.Many2one(comodel_name='pos_route_config.create_report', string='Variables', readonly=True)

    #date = fields.Date(string='Fecha de creaciónA')
    departure_date = fields.Datetime(string='Fecha de creación', default=fields.Datetime.now()) #Salida Comentar
    name = fields.Char(string='Referencia de ruta', default='Nuevo')
    #fecha_filtro = fields.Date(string='Fecha de configuración de rutaJ: ', default=fields.Date.today())
    #fecha_reporte = fields.Date(string='Fecha  reporteJ: ', default=fields.Date.today())

    #route_config_id = fields.Many2one(string='Route configuration', comodel_name='pos_route_config.route_config')
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