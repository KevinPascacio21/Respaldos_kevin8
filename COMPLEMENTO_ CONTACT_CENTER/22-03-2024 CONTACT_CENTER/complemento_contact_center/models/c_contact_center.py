# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from odoo import api, fields, models

# #Modelo que hereda al sale order (contact center) 
# class complemento_contact_center(models.Model):
#     _inherit = 'sale.order'


#     # Tracking fields
#     name = fields.Char(tracking=True)
#     currency_id = fields.Many2one(tracking=True)
#     company_id = fields.Many2one(tracking=True)

#Heredo los campos de sale order(contact center) y en caso de que sean editados, que se muestren en la seccion de abajo
       # partner_id = fields.Many2one(tracking=True) #tracking true para que el campo sea rastreado para detectar cambios SI SE MUESTRA
    # x_studio_telefono = fields.Char(string="Telefono")
    # x_studio_direccin_de_contacto = fields.Char(string="Direccion de contacto")
    # x_studio_colonia = fields.Char(string="Colonia")
    # x_studio_folio = fields.Integer(tracking=True)
    # x_studio_estatus_pedido = fields.Selection(tracking=True,
    #     selection=[('Recibido', 'Recibido'), #izq: lo que se verá en el reporte (excel), der: lo que se mostrará en la vista al jalar los datos
    #                ('Transmitido', 'Transmitido'),
    #                ('Confirmado', 'Confirmado'), 
    #                ('Cancelado', 'Cancelado')])
    # date_order = fields.Datetime(string="Fecha de la orden")
    # pricelist_id = fields.Many2one(string="Lista de precios")
    # payment_term_id = fields.Many2one(string="Terminos de pago")
    # x_studio_punto_de_venta = fields.Many2one(tracking=True)
    # # x_studio_tipo_almacn = fields.Selection#(string='Tipo Almacén',
    # #     selection=[('Almacén', 'Almacén')
    # #                ('Portátil', 'Portátil'), 
    # #                ('Autotanque', 'Autotanque'),
    # #                ('Carburación', 'Carburación')])
    # # x_studio_mtodos_de_contacto = fields.Selection(string='Tipo Almacén',
    # #     selection=[('Vía telefónica', 'Vía telefónica'), 
    # #                ('WhatsApp', 'WhatsApp'),
    # #                ('Facebook messenger', 'Facebook messenger')
    # #                ('Página Web', 'Página Web'),
    # #                ('App', 'App')])
    # x_studio_punto_de_venta = fields.Many2one(string="Punto de venta")

    # product_id = fields.Many2one(string="Producto")
    # name = fields.Text(string="Descripcion")
    # product_uom_qty = fields.Float(string="Cantidad")
    # qty_delivered = fields.Float(string="Entregado")
    # qty_invoiced = fields.Float(string="Facturado")
    # product_uom = fields.Many2one(string="UDM")
    # price_unit = fields.Float(string="Precio unitario")
    # tax_id = fields.Many2many(string="Impuestos")
    #price_subtotal= fields.Monetary(string="Subtotal")



    


#Modelo que agrega campos necesarios al respartner (datos del modelo)
# class c_center(models.Model):
#     _inherit = 'res.partner'

#     x_referencia = fields.Char(tracking=True)

#     # @api.model
#     # def create(self, vals):
#     #     record = super(c_center, self).create(vals)
    #     self.env['field_history'].create({
    #         'field_name': 'my_field',
    #         'old_value': False,
    #         'new_value': vals.get('my_field'),
    #         'modified_date': fields.Datetime.now(),
    #         'record_id': record.id,
    #     })
    #     return record

    # def write(self, vals):
    #     old_vals = {field: getattr(self, field) for field in vals.keys()}
    #     res = super(c_center, self).write(vals)
    #     for field, new_value in vals.items():
    #         old_value = old_vals.get(field)
    #         if old_value != new_value:
    #             self.env['field_history'].create({
    #                 'field_name': field,
    #                 'old_value': old_value,
    #                 'new_value': new_value,
    #                 'modified_date': fields.Datetime.now(),
    #                 'record_id': self.id,
    #             })
    #     return res


#Class Historial para almacenar el registro de las modificaciones/ediciones del cliente
# class FieldHistory(models.Model):
#     _name = 'field_history'
#     _description = 'Field Modification History'

#     field_name = fields.Char(string='Field Name', required=True)
#     old_value = fields.Char(string='Old Value')
#     new_value = fields.Char(string='New Value')
#     modified_date = fields.Datetime(string='Modification Date')
#     record_id = fields.Integer(string='Record ID', required=True)






























#Campos ID´s y en español------------------------------------------------------------------------------
# partner_id -> Cliente ---> Meter un campo nuevo llamado "Referencias" REFERENCE CHAR (casa blanca de 2 pisos) que este dentro del campo de cliente
# x_studio_telefono -> Telefono
# x_studio_direccin_de_contacto -> Direccion de contacto
# x_studio_colonia -> Colonia
# x_studio_folio -> Folio
# x_studio_estatus_pedido -> Estatus pedido
# date_order -> Fecha de la orden
# pricelist_id -> Lista de precios
# payment_term_id -> Terminos de pago (deshabilitado)
# x_studio_punto_de_venta -> Punto de venta
# x_studio_tipo_almacn -> Tipo de almacen
# x_studio_mtodos_de_contacto -> Metodo de contacto
# x_studio_punto_de_venta -> Punto de venta 


# product_id -> Producto
# name -> Descripcion
# product_uom_qty -> Cantidad
# qty_delivered -> Entregado
# qty_invoiced -> Facturado
# product_uom -> UDM
# price_unit -> Precio unitario
# tax_id -> Impuestos
# price_subtotal -> Subtotal