# -*- coding: utf-8 -*-

# from datetime import datetime, timedelta
# from functools import partial
# from itertools import groupby
from odoo import api, fields, models
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class pos_order_cancel(models.Model):
    _inherit = 'pos.order'

    x_studio_cancelado = fields.Boolean(default=False)
    _logger.warning("Fuera de la funcion para comparacion de condiciones")
    
    @api.onchange('x_studio_cancelado')
    def get_cancel_order_validation_and_state(self):
        _logger.warning("Dentro de la función para comparación de condiciones")
        for record in self:
            if record.x_studio_cancelado:
                if record.validation == 'Validado' and record.state not in ('paid', 'draft'): # Validado pero sin pago/nuevo (no cancelar)
                    _logger.warning("VALIDADO PERO SIN PAGADO/NUEVO")
                    raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
                if record.validation == 'Validado' and record.state in ('paid', 'draft'): # Validado con pago/nuevo (no cancelar)
                    _logger.warning("VALIDADO, PAGADO Y NUEVO, NO CANCELAR ORDEN")
                    raise UserError("No se puede cancelar la orden porque el registro ya está validado") 
                if record.validation != 'Validado' and record.state in ('paid', 'draft'): # Sin validar pero con pago/nuevo (cancelar)
                    record.x_studio_cancelado = True
                    _logger.warning("NO VALIDADO, PAGADO Y NUEVO, CANCELAR ORDEN")
                    return {'warning': {'title': 'Mensaje de confirmación', 'message': 'Orden cancelada correctamente'}}
                if record.validation != 'Validado' and record.state not in ('paid', 'draft'):   # Sin validar y sin pago/nuevo(cancelar)
                    record.x_studio_cancelado = True
                    _logger.warning("NO VALIDADO, SIN PAGADO/NUEVO, CANCELAR ORDEN K")
                    return {'warning': {'title': 'Mensaje de confirmación', 'message': 'Orden cancelada correctamente'}}