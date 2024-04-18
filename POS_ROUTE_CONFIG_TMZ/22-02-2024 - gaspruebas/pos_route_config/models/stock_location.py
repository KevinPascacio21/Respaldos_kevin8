from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'
    

    x_studio_tipo_almacn = fields.Selection(string='Tipo Almacén',
        selection=[('Almacén', 'Almacén'), 
                   ('Portátil', 'Portátil'), 
                   ('Autotanque', 'Autotanque'), 
                   ('Carburación', 'Carburación')])
