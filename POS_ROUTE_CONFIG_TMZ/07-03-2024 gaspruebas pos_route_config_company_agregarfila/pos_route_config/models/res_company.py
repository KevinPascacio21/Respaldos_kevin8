from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    short_name = fields.Char(string='Short name')
