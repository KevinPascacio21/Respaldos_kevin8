# -*- coding: utf-8 -*-
# from odoo import http


# class PosRouteConfig(http.Controller):
#     @http.route('/pos_route_config/pos_route_config/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_route_config/pos_route_config/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_route_config.listing', {
#             'root': '/pos_route_config/pos_route_config',
#             'objects': http.request.env['pos_route_config.pos_route_config'].search([]),
#         })

#     @http.route('/pos_route_config/pos_route_config/objects/<model("pos_route_config.pos_route_config"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_route_config.object', {
#             'object': obj
#         })
