# -*- coding: utf-8 -*-

# from datetime import datetime, timedelta
# from functools import partial
# from itertools import groupby
from odoo import api, fields, models
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


# #Modlo que hereda al sale order (contact center) 
class pos_order_cancel(models.Model):
#     _name = 'pos_order_cancel.pos_order_cancel'
#     _description = 'pos_order_cancel.pos_order_cancel'
    _inherit = 'pos.order'

    # name = fields.Char()
    # currency_id = fields.Many2one(tracking=True)
    # company_id = fields.Many2one(tracking=True)

    # validation = fields.Char(related='pos_order.validation')
    # validation = fields.Char(tracking=True)
    # state = fields.Selection(
    #     selection=[('draft', 'Nuevo'),
    #                ('cancel', 'Cancelado'),
    #                ('paid', 'Pagado'),
    #                ('done', 'Publicado'), 
    #                ('invoiced', 'Facturado')],  tracking=True)
    cancel_order_validation = fields.Boolean(string="Cancelar orden de validación", compute="get_cancel_order_validation")
    # cancel_order_status = fields.Char(string="Cancelar orden de estatus", compute="get_cancel_order_status")
    cancel_orden_message_valid = fields.Boolean(string="Cancelar Orden", readonly=True)
    # cancel_orden_message_state = fields.Boolean(string="Cancelar Orden", readonly=True)


    @api.onchange('x_studio_cancelado')
    # @api.depends_context('validation')
    def get_cancel_order_validation(self):
        _logger.warning("verificar validacion para realizar funcion")
        for record in self:
            record.cancel_order_validation = False
            if record.x_studio_cancelado:
                record.cancel_orden_message_valid = True
                raise UserError("ORDEN CANCELADA") 
            if record.state == 'Validado':  # Asumiendo que 'state' es el campo que indica el estado de la orden
                record.cancel_orden_message_valid = True
                raise UserError("No se puede cancelar la orden porque el registro ya está validado")
            else:
                record.cancel_order_validation = False
                record.cancel_orden_message_valid = False


    # @api.depends('state')
    # def get_cancel_order_status(self):
    #     for record in self:
    #         record.cancel_order_status = False
    #         if record.state not in ('paid', 'draft'):
    #             record.cancel_orden_message_state = True
    #             raise UserError("Solo se puede cancelar la orden si el estatus es pagado o nuevo") 
    #         else:
    #             record.cancel_orden_message_state = False


    #Funciones para validar en caso de que se presione el boton cancelar orden y si el archivo esta validado
    # @api.depends('validation')
    # def get_cancel_order_validation(self):
    #     _logger.warning("verificar validacion para realizar funcion")
    #     for record in self:
    #         record.cancel_order_validation = False
    #         if record.validation == 'Validado':
    #             record.cancel_orden_validation = True
    #         else:
    #             record.cancel_orden_validation = False
    
    # def cancel_order(self):
    #     for order in self:
    #         if order.validation == 'Validado':
    #             raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
    #         else:
    #             order.action_cancel()

    

# #otras funciones simplificadas
#     @api.depends('validation')
#     def get_cancel_order_validation(self):
#         for record in self:
#             record.cancel_order_validation = record.validation == 'Validado'

#     def cancel_order(self):
#         for order in self:
#             if order.validation == 'Validado':
#                 raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
#             order.action_cancel()
            

#     @api.depends('state')
#     def get_cancel_order_validation(self):
#         for record in self:
#             record.cancel_order_validation = record.state not in ('paid', 'draft')

#     def cancel_order(self):
#         for order in self:
#             if order.state not in ('paid', 'draft'):
#                 raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
#             order.action_cancel()

    # @api.depends('state')
    # def get_cancel_order_status(self):
    #     for record in self:
    #         record.cancel_order_status = False
    #         if record.state not in ('paid', 'draft'):
    #             record.cancel_orden_message_state = True
    #             raise UserError("Solo se puede cancelar la orden si el estatus es pagado o nuevo") 
    #         else:
    #             record.cancel_orden_message_state = False





    
    # @api.depends('validation')
    # def _compute_cancel_order_validation(self):
    #     for record in self:
    #         record.cancel_order_validation = False
    #         if record.validation == 'Validado':
    #             record.cancel_orden_message_valid = True
    #         else:
    #             record.cancel_orden_message_valid = False

    # @api.depends('state')
    # def _compute_cancel_order_status(self):
    #     for record in self:
    #         record.cancel_order_status = False
    #         if record.state not in ('paid', 'draft'):
    #             record.cancel_orden_message_state = True
    #         else:
    #             record.cancel_orden_message_state = False

    # @api.constrains('validation')
    # def _check_validation(self):
    #     for record in self:
    #         if record.validation == 'Validado':
    #             raise UserError(("No se puede cancelar la orden porque el registro ya está validado"))

    # @api.constrains('state')
    # def _check_state(self):
    #     for record in self:
    #         if record.state not in ('paid', 'draft'):
    #             raise UserError(("Solo se puede cancelar la orden si el estatus es pagado o nuevo"))