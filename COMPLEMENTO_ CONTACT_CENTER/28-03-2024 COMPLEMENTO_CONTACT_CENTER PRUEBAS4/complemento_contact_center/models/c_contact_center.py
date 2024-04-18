# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
from odoo import api, fields, models

# #Modelo que hereda al sale order (contact center) 
class complemento_contact_center(models.Model):
    _inherit = 'sale.order'


    # Tracking fields
    name = fields.Char(tracking=True)
    currency_id = fields.Many2one(tracking=True)
    company_id = fields.Many2one(tracking=True)

#Heredo los campos de sale order(contact center) y en caso de que sean editados, que se muestren en la seccion de abajo
    # partner_id = fields.Many2one(tracking=True)  #Dejarlo asi
    # x_studio_telefono = fields.Char(readonly=False, tracking=True) #Dejarlo asi
    # x_studio_direccin_de_contacto = fields.Char(string="Direccion de contacto")  #Dejarlo asi
    # x_studio_colonia = fields.Char(string="Colonia") #Dejarlo asi

    x_studio_folio = fields.Integer(tracking=True)
    # x_studio_estatus_pedido = fields.Selection(
    #     selection=[('Recibido', 'Recibido'),
    #                ('Transmitido', 'Transmitido'),
    #                ('Confirmado', 'Confirmado'), 
    #                ('Cancelado', 'Cancelado')],  tracking=True)
    # validity_date = fields.Date(tracking=True) no existe
    date_order = fields.Datetime(readonly=False, tracking=True)
    pricelist_id = fields.Many2one(readonly=False, tracking=True)
    payment_term_id = fields.Many2one(readonly=False, tracking=True)
    # x_studio_punto_de_venta = fields.Many2one(tracking=True)
    x_studio_tipo_almacn = fields.Selection(
        selection=[('Almacén', 'Almacén'),
                   ('Portátil', 'Portátil'), 
                   ('Autotanque', 'Autotanque'),
                   ('Carburación', 'Carburación')], tracking=True)
    # x_studio_mtodos_de_contacto = fields.Selection(
    #     selection=[('Vía telefónica', 'Vía telefónica'), 
    #                ('WhatsApp', 'WhatsApp'),
    #                ('Facebook messenger', 'Facebook messenger')
    #                ('Página Web', 'Página Web'),
    #                ('App', 'App')],  tracking=True)
    # x_studio_punto_de_venta = fields.Many2one(string="Punto de venta")


#------pestaña de Lineas de la orden para heredar los campos de sale.order.line------------------------------------
    order_line = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string='Order Lines',
        copy=True
    )
    # product_id = fields.Many2one(readonly=False, tracking=True) #No esta en sale order
    # name = fields.Text(tracking=True)
    # product_uom_qty = fields.Float(tracking=True) #
    # qty_delivered = fields.Float(readonly=False, tracking=True)
    # qty_invoiced = fields.Float(readonly=False, tracking=True)
    # product_uom = fields.Many2one(readonly=False, tracking=True)
    # price_unit = fields.Float(tracking=True)
    
    # tax_id = fields.Many2many(tracking=True)
    # price_subtotal= fields.Monetary(tracking=True)



   # Metodo para cambios de la lista de list_order
    # def write(self, vals):
    #     if 'item_ids' in vals:
    #         for record in self:
    #             # Initial values to compare
    #             initial_values = [{
    #                 'product_id': rec.product_id, 
    #                 'name':rec.name, 
    #                 "product_uom_qty":rec.product_uom_qty, 
    #                 'qty_delivered':rec.qty_delivered, 
    #                 'qty_invoiced':rec.qty_invoiced, 
    #                 'product_uom':rec.product_uom, 
    #                 'price_unit':rec.price_unit, 
    #                 'tax_id': rec.tax_id, 
    #                 'price_subtotal':rec.price_subtotal, 
    #                 'dip': rec.dip, 
    #                 'iva_precio': rec.iva_precio, 
    #                 'applied_on': rec.applied_on
    #             } for rec in record.item_ids ]
    #             initial_value = ''.join(f"- Nombre: {rec.name}, Cantidad minima: {rec.min_quantity}, Precio: {rec.price}, Fecha inicio: {rec.date_start}, Fecha final: {rec.date_end}, Comision: {rec.comision}, Comision acumulada: {rec.comision_acumulada}, Descuento: {rec.descuento}, Subsidio: {rec.subsidio}, DIP: {rec.dip},  IVA: {rec.iva_precio if rec.applied_on in ['3_global', '2_product_category'] else 'N/A'} <br/>" for rec in record.item_ids)
    #             init_size = len(record.item_ids)
        
    #             # super need to be before new_value
    #             result = super().write(vals) 
        
    #             # New values to compare
    #             new_value = ''.join(f"- Nombre: {rec.name}, Cantidad minima: {rec.min_quantity}, Precio: {rec.price}, Fecha inicio: {rec.date_start}, Fecha final: {rec.date_end}, Comision: {rec.comision}, Comision acumulada: {rec.comision_acumulada}, Descuento: {rec.descuento}, Subsidio: {rec.subsidio}, DIP: {rec.dip}, IVA: {rec.iva_precio if rec.applied_on in ['3_global', '2_product_category'] else 'N/A'}<br/>" for rec in record.item_ids)
    #             new_values = [{
    #                 'name': rec.name, 
    #                 'min_quantity':rec.min_quantity, 
    #                 "price":rec.price, 
    #                 'date_start':rec.date_start, 
    #                 'date_end':rec.date_end, 
    #                 'comision':rec.comision, 
    #                 'comision_acumulada':rec.comision_acumulada, 
    #                 'descuento': rec.descuento, 
    #                 'subsidio':rec.subsidio, 
    #                 'dip': rec.dip, 
    #                 'iva_precio': rec.iva_precio,
    #                 'applied_on': rec.applied_on
    #             } for rec in record.item_ids]
    #             new_size = len(record.item_ids)
    #             last_item = None
        
    #             # validate if there is a new item
    #             if new_size > 0:
    #                 iva = None
    #                 if record.item_ids[new_size - 1].applied_on in ['3_global', '2_product_category']:
    #                     iva = f"IVA: {record.item_ids[new_size - 1].iva_precio}" 
    #                 else:
    #                     iva = 'IVA: N/A'           
    #                 last_item = f"- Nombre: {record.item_ids[new_size - 1].name}, Cantidad minima: {record.item_ids[new_size - 1].min_quantity}, Precio: {record.item_ids[new_size - 1].price}, Fecha inicio: {record.item_ids[new_size - 1].date_start}, Fecha final: {record.item_ids[new_size - 1].date_end}, Comision: {record.item_ids[new_size - 1].comision}, Comision acumulada: {record.item_ids[new_size - 1].comision_acumulada}, Descuento: {record.item_ids[new_size - 1].descuento}, Subsidio: {record.item_ids[new_size - 1].subsidio}, DIP: {record.item_ids[new_size - 1].dip}, {iva}"
          
    #             # String formatted to log when an item has changed 
    #             message_body = self.compare_items(initial_values, new_values)
        
    #             # if a new item is added
    #             if init_size < new_size:
    #                 if init_size == 0:
    #                     body = f"Se agregaron estas normas: <br/> {new_value}"
    #                     record.message_post(body=body)
    #                 else:
    #                     body = f"Se creo una norma: <br/> {last_item}"
    #                     record.message_post(body=body)
    #             # if an item is deleted
    #             elif init_size > new_size:
    #                 body = f"Se eliminaron normas: <br/> <strong>Antes:</strong> <br/> {initial_value}<br/><br/> <strong>Resultado:</strong><br/> {new_value}"
    #                 record.message_post(body=body)
    #             # if an item is modified 
    #             else: 
    #                 if initial_value != new_value:
    #                     for message in message_body:
    #                         record.message_post(body=f"Se modifico una norma: <br/> <strong>Antes:</strong> <br/>{message[0]}<br/><br/>  <strong>Resultado:</strong><br/> {message[1]}")
    #             return result
    #     else:
    #         return super().write(vals)


    #------------------------------pestaña de Más informacón:------------------------------------
    #Ventas:
    user_id = fields.Many2one(tracking=True) #Vendedor BIEN
    # team_id = fields.Many2one(tracking=True) #Equipo de ventas NO FILTRA NINGUN DATO
    company_id = fields.Many2one(tracking=True) #Empresa SIN PERMISOS
    require_signature = fields.Boolean(readonly=False, tracking=True) #Firma en linea
    require_payment = fields.Boolean(readonly=False, tracking=True) #Pago en linea
    client_order_ref = fields.Char(tracking=True) #Referencia del cliente BIEN
    tag_ids = fields.Many2many(tracking=True) #Etiquetas NO ME MUESTRA SU HISTORIAL
    #Facturación:
    fiscal_position_id = fields.Many2one(tracking=True) #Posición fiscal BIEN
    analytic_account_id = fields.Many2one(tracking=True) #Cuenta analítica BIEN
    invoice_status = fields.Selection( #Estado de factura BIEN
        selection=[('upselling', 'Oportunidad de venta adicional'),
                   ('invoiced', 'Facturado por completo'),
                   ('to invoice', 'A facturar'), 
                   ('no', 'Nada que facturar')], readonly=False,  tracking=True)
    #Entrega:
    warehouse_id = fields.Many2one(readonly=False, tracking=True) #Almacén NO ME DEJA EDITAR EL CAMPO
    incoterm = fields.Many2one(tracking=True) #Incoterm BIEN
    picking_policy = fields.Selection( #Política de entrega NO SE PUEDE EDITAR
        selection=[('direct', 'Lo antes posible'), 
                   ('one', 'Cuando todos los productos estén listos')], readonly=False, tracking=True)    
    commitment_date = fields.Datetime(tracking=True) #Fecha de entrega BIEN
    #Reportes:
    origin = fields.Char(tracking=True) #Documento de origen BIEN
    opportunity_id = fields.Many2one(tracking=True) #Oportunidad BIEN
    campaign_id = fields.Many2one(tracking=True) #Campaña BIEN
    medium_id = fields.Many2one(tracking=True) #Medio  BIEN
    source_id = fields.Many2one(tracking=True) #Origen BIEN
  

    # #------------------------------pestaña de Firma del cliente:------------------------------------
    signed_by = fields.Char(tracking=True) #Firmado por BIEN
    signed_on = fields.Datetime(tracking=True) #Firmado BIEN
    signature = fields.Binary(tracking=True) #Firma

    #Campo computado para que x_referencia (de resPartner) se muestre en la vista kambal (de sale order)
    x_referencia_partner = fields.Char(string='Referencia del Socio', compute='_compute_referencia_partner')

    @api.depends('partner_id.x_referencia')
    def _compute_referencia_partner(self):
        for order in self:
            order.x_referencia_partner = order.partner_id.x_referencia

    # @api.depends('partner_id.product_uom_qty')
    # def _compute_product_uom_qty_partner(self):
    #     for order in self:
    #         order.product_uom_qty_partner = order.partner_id.product_uom_qty



    

#Modelo que agrega campos necesarios al respartner (datos del modelo)
class c_center(models.Model):
    _inherit = 'res.partner'

    x_referencia = fields.Char(tracking=True)


class table_lineas_orden(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(readonly=False, tracking=True) #No esta en sale order
    name = fields.Text(tracking=True)
    product_uom_qty = fields.Float(tracking=True) #
    qty_delivered = fields.Float(readonly=False, tracking=True)
    qty_invoiced = fields.Float(readonly=False, tracking=True)
    product_uom = fields.Many2one(readonly=False, tracking=True)
    price_unit = fields.Float(tracking=True)
    tax_id = fields.Many2many(tracking=True)
    price_subtotal= fields.Monetary(tracking=True)