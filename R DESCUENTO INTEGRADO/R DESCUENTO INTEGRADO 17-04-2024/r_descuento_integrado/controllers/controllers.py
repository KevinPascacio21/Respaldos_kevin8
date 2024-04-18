# -*- coding: utf-8 -*-
# from odoo import http


# class ReporteDescuentoIntegrado(http.Controller):
#     @http.route('/reporte_descuento_integrado/reporte_descuento_integrado/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reporte_descuento_integrado/reporte_descuento_integrado/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reporte_descuento_integrado.listing', {
#             'root': '/reporte_descuento_integrado/reporte_descuento_integrado',
#             'objects': http.request.env['reporte_descuento_integrado.reporte_descuento_integrado'].search([]),
#         })

#     @http.route('/reporte_descuento_integrado/reporte_descuento_integrado/objects/<model("reporte_descuento_integrado.reporte_descuento_integrado"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reporte_descuento_integrado.object', {
#             'object': obj
#         })
