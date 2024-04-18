# -*- coding: utf-8 -*-
# from odoo import http


# class PosRouteConfigTmz(http.Controller):
#     @http.route('/pos_route_config_tmz/pos_route_config_tmz/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_route_config_tmz/pos_route_config_tmz/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_route_config_tmz.listing', {
#             'root': '/pos_route_config_tmz/pos_route_config_tmz',
#             'objects': http.request.env['pos_route_config_tmz.pos_route_config_tmz'].search([]),
#         })

#     @http.route('/pos_route_config_tmz/pos_route_config_tmz/objects/<model("pos_route_config_tmz.pos_route_config_tmz"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_route_config_tmz.object', {
#             'object': obj
#         })
