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
    _inherit = 'pos.order'

#para CANCELAR ORDEN:
@api.onchange('x_studio_cancelado')
def get_cancel_order_validation_and_state(self):
    for record in self:
        if record: #.x_studio_cancelado:
            _logger.warning("AQUI ESTA ENTRENDO A LA FUNCION DE CANCELACION DE ORDEN DEPENDIENDO LA CONDICION")
            if record.validation == 'Validado' and record.state not in ('paid', 'draft'): #Validado pero sin pago/nuevo (no bede de dejar)
                raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
            if record.validation == 'Validado' and record.state in ('paid', 'draft'): #Validado con pago/nuevo (no debe de dejar)
                raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
            if record.validation != 'Validado' and record.state in ('paid', 'draft'): #Sin validar pero con pago/nuevo
                # record.unlink()
                raise UserError("ORDEN CANCELADA CORRECTAMENTE") 
            if record.validation != 'Validado' and record.state not in ('paid', 'draft'):   #Sin validar y sin pago/nuevo
                # record.unlink()
                raise UserError("ORDEN CANCELADA CORRECTAMENTE")