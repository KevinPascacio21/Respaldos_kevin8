from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    _sql_constraints = [
        ('distribution_point_name_unique', 'unique(distribution_point_name, company_id)',
         'There can only be one distribution point name per company')]

    can_start_session = fields.Boolean(string='Can start POS session?', default=True)
    route_config_state = fields.Selection(string='Route Config Status', compute="_compute_route_state",
        selection=[('new', 'Without route'), ('start', 'Route Configuration'), ('sale', 'Sales'), 
                    ('reception', 'Route Reception'), ('concil', 'Sale Conciliation'), ('finish', 'Cash Box Closed')])
    distribution_point_name = fields.Char(string='Distribution point name')
    is_gaspar_available = fields.Boolean(string='Is Gaspar Available?', default=True)
    
    # unit_name = fields.Char(string="Unit name")
    # gaspar_server = fields.Many2one(string="Gaspar", comodel_name="pos_route_config.gaspar")
    #TODO Agregar al form de pos.config
    
    def _compute_route_state(self):
        for config in self:
            route = self.env['pos_route_config.route_config'].search([('state', '!=', 'finish'), ('pos_config_id', '=', config.id)])
            if route:
                config.route_config_state = route.state
            else:
                config.route_config_state = 'new'