# -*- coding: utf-8 -*-
# from odoo import http


# class ComplContactCenter(http.Controller):
#     @http.route('/compl_contact_center/compl_contact_center/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/compl_contact_center/compl_contact_center/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('compl_contact_center.listing', {
#             'root': '/compl_contact_center/compl_contact_center',
#             'objects': http.request.env['compl_contact_center.compl_contact_center'].search([]),
#         })

#     @http.route('/compl_contact_center/compl_contact_center/objects/<model("compl_contact_center.compl_contact_center"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('compl_contact_center.object', {
#             'object': obj
#         })
