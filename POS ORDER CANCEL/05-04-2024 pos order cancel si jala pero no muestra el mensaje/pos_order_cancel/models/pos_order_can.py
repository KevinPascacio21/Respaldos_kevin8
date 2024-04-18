# -*- coding: utf-8 -*-

# from datetime import datetime, timedelta
# from functools import partial
# from itertools import groupby
from odoo import api, fields, models
from odoo.exceptions import UserError
# import logging
# _logger = logging.getLogger(__name__)


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
    # cancel_order_validation = fields.Char(string="Cancelar orden de validación", compute="get_cancel_order_validation")
    # cancel_order_status = fields.Char(string="Cancelar orden de estatus", compute="get_cancel_order_status")
    # cancel_orden_message_valid = fields.Boolean(string="Cancelar Orden", readonly=True)
    # cancel_orden_message_state = fields.Boolean(string="Cancelar Orden", readonly=True)



    #Funciones para validar en caso de que se presione el boton cancelar orden y si el archivo esta validado
    @api.depends('validation')
    def cancel_order(self):
        for order in self:
            order.cancel_order_validation = False
            if order.validation == 'Validado':
                # record.cancel_orden_message_valid = True
                raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
            else:
                # record.cancel_orden_message_valid = False
                # order.write({'state': 'cancel'})
                super(pos_order_cancel, order).cancel_order()

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
    # # @api.depends_context('validation')
    # def get_cancel_order_validation(self):
    #     _logger.warning("verificar validacion para realizar funcion")
    #     for record in self:
    #         record.cancel_order_validation = False
    #         if record.validation == 'Validado':
    #         # if self.env.context.get('validation') == 'Validado':
    #             record.cancel_orden_message_valid = True
    #             raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
    #         else:
    #             record.cancel_orden_message_valid = False

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