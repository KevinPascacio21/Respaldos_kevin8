# -*- coding: utf-8 -*-
# from odoo import http


# class PosOrderCancel(http.Controller):
#     @http.route('/pos_order_cancel/pos_order_cancel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_order_cancel/pos_order_cancel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_order_cancel.listing', {
#             'root': '/pos_order_cancel/pos_order_cancel',
#             'objects': http.request.env['pos_order_cancel.pos_order_cancel'].search([]),
#         })

#     @http.route('/pos_order_cancel/pos_order_cancel/objects/<model("pos_order_cancel.pos_order_cancel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_order_cancel.object', {
#             'object': obj
#         })
