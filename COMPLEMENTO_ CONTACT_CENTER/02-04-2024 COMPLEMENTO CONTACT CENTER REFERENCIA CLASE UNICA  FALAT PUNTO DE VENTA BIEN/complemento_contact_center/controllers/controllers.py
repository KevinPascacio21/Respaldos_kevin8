# -*- coding: utf-8 -*-
# from odoo import http


# class ComplementoContactCenter(http.Controller):
#     @http.route('/complemento_contact_center/complemento_contact_center/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/complemento_contact_center/complemento_contact_center/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('complemento_contact_center.listing', {
#             'root': '/complemento_contact_center/complemento_contact_center',
#             'objects': http.request.env['complemento_contact_center.complemento_contact_center'].search([]),
#         })

#     @http.route('/complemento_contact_center/complemento_contact_center/objects/<model("complemento_contact_center.complemento_contact_center"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('complemento_contact_center.object', {
#             'object': obj
#         })
