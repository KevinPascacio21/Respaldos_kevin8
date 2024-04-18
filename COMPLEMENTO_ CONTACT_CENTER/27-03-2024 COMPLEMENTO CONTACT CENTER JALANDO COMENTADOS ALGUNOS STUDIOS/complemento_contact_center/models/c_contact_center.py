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
    # name = fields.Char(tracking=True) #Parte del cliente, no se debe de editar
    # partner_id = fields.Many2one(tracking=True)  #Parte del cliente, no se debe de editar
    # x_studio_telefono = fields.Char(readonly=False, tracking=True) #Parte del cliente, no se debe de editar
    # x_studio_direccin_de_contacto = fields.Char(string="Direccion de contacto")  #Parte del cliente, no se debe de editar
    # x_studio_colonia = fields.Char(string="Colonia")  #Parte del cliente, no se debe de editar

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


#------------------------------pestaña de Lineas de la orden:------------------------------------
    # product_id = fields.Many2one(tracking=True) #No esta en sale order
    # name = fields.Text(string="Descripcion")
    # product_uom_qty = fields.Float(tracking=True) #
    # qty_delivered = fields.Float(string="Entregado")
    # qty_invoiced = fields.Float(string="Facturado")
    # product_uom = fields.Many2one(string="UDM")
    # price_unit = fields.Float(tracking=True)
    # tax_id = fields.Many2many(tracking=True)
    #price_subtotal= fields.Monetary(string="Subtotal")

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
    # signature = fields.Binary(tracking=True) #Firma


    x_referencia_partner = fields.Char(string='Referencia del Socio', compute='_compute_referencia_partner')

    @api.depends('partner_id.x_referencia')
    def _compute_referencia_partner(self):
        for order in self:
            order.x_referencia_partner = order.partner_id.x_referencia



    


#Modelo que agrega campos necesarios al respartner (datos del modelo)
class c_center(models.Model):
    _inherit = 'res.partner'

    x_referencia = fields.Char(tracking=True)





# class lineas_orden(models.Model):
#     _inherit = 'modelo hjeredado'

    # product_id = fields.Many2one(tracking=True)
    # name = fields.Text(string="Descripcion")
    # qty_delivered = fields.Float(string="Entregado")
    # qty_invoiced = fields.Float(string="Facturado")
    # product_uom = fields.Many2one(string="UDM")
    # price_unit = fields.Float(tracking=True)
    # tax_id = fields.Many2many(tracking=True)
    #price_subtotal= fields.Monetary(string="Subtotal")
















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