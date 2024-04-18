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
    # x_studio_cancelado = fields.Boolean(readonly=True)
    # validation = fields.Char(related='pos_order.validation')
    # validation = fields.Char(tracking=True)
    # state = fields.Selection(
    #     selection=[('draft', 'Nuevo'),
    #                ('cancel', 'Cancelado'),
    #                ('paid', 'Pagado'),
    #                ('done', 'Publicado'), 
    #                ('invoiced', 'Facturado')],  tracking=True)
    # cancel_order_validation = fields.Boolean(string="Cancelar orden de validación", compute="get_cancel_order_validation")
    # cancel_order_status = fields.Char(string="Cancelar orden de estatus", compute="get_cancel_order_status")
    # cancel_orden_message_valid = fields.Boolean(string="CanOrd", readonly=True)
    # cancel_orden_message_state = fields.Boolean(string="Cancelar Orden", readonly=True)

    @api.onchange('x_studio_cancelado')
    def get_cancel_order_validation(self):
        _logger.warning("AQUI ESTA ENTRENDO A LA FUNCION DE CANCELACION DE ORDEN DEPENDIENDO LA CONDICION")
        for record in self:
            if record.x_studio_cancelado:
                if record.validation == 'Validado':
                    raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
                # if record.state not in ('paid', 'draft'):
                #     raise UserError("No se puede cancelar la orden porque el estado es 'Pagado' o 'Borrador'")
                # record.x_studio_cancelado = True #Para que este desactivado el toggle cancelado y no me borre la orden
            if record.x_studio_cancelado:
                if record.validation != 'Validado':
                    raise UserError("ORDEN CANCELADA CORRECTAMENTE")
                record.unlink()
                # record.x_studio_cancelado = False
                # if record.state in ('paid', 'draft'):
                    # raise UserError("ORDEN CANCELADA CORRECTAMENTE")



#UN SOLO IF PARA ALGUNA DE LAS 2 OPCIONES QUE SEAN CORRECTAS PARA CANCELAR ORDEN
    # @api.onchange('x_studio_cancelado')
    # def get_cancel_order_validation_and_state(self):
    #     _logger.warning("AQUI ESTA ENTRENDO A LA FUNCION DE CANCELACION DE ORDEN DEPENDIENDO LA CONDICION")
    #     for record in self:
    #         if record.x_studio_cancelado:
    #             if record.validation == 'Validado' or record.state in ('paid', 'draft'):
    #                 raise UserError("No se puede cancelar la orden porque el registro ya está validado o en estatus nuevo/pagado") 
    #             # record.x_studio_cancelado = True #Para que este desactivado el toggle cancelado y no me borre la orden
    #         if record.x_studio_cancelado:
    #             if record.validation != 'Validado'or record.state not in ('paid', 'draft'):
    #                 raise UserError("ORDEN CANCELADA CORRECTAMENTE")
    #             # record.x_studio_cancelado = False
    #             # if record.state in ('paid', 'draft'):
    #                 # raise UserError("ORDEN CANCELADA CORRECTAMENTE")











    # @api.onchange('x_studio_cancelado')#NO entrea a la funcion
    # def get_cancel_order_validation(self):
    #     _logger.warning("AQUI ESTA ENTRENDO A LA FUNCION DE CANCELACION DE ORDEN DEPENDIENDO LA CONDICION")
    #     for record in self:
    #         record.cancel_order_validation = False
    #         if record.validation == 'Validado':  # Asumiendo que 'state' es el campo que indica el estado de la orden
    #             record.cancel_orden_message_valid = False
    #             raise UserError("No se puede cancelar la orden porque el registro ya está validado")
    #         if record.x_studio_cancelado:
    #             record.cancel_orden_message_valid = True
    #             raise UserError("ORDEN CANCELADA POR KEVIN") 
            # else:
            #     record.cancel_order_validation = False
            #     record.cancel_orden_message_valid = False
            #     raise UserError("La orden se cancelo con exito")

    # @api.depends('state')
    # def get_cancel_order_status(self):
    #     for record in self:
    #         record.cancel_order_status = False
    #         if record.state not in ('paid', 'draft'):
    #             record.cancel_orden_message_state = True
    #             raise UserError("Solo se puede cancelar la orden si el estatus es pagado o nuevo") 
    #         else:
    #             record.cancel_orden_message_state = False

    # @api.depends('state')
    # def get_cancel_order_status(self):
    #     for record in self:
    #         record.cancel_order_status = False
    #         if record.state not in ('paid', 'draft'):
    #             record.cancel_orden_message_state = True
    #             raise UserError("Solo se puede cancelar la orden si el estatus es pagado o nuevo") 
    #         else:
    #             record.cancel_orden_message_state = False



