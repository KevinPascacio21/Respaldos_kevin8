from odoo import api, fields, models


class GasparServer(models.Model):
    _name = 'pos_route_config.gaspar_server'
    _description = 'Gaspar Server Description'

    name = fields.Char(string='Name')
    external_id = fields.Char(string='External ID')
    
