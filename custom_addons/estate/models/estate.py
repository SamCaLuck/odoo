from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class RealEstate(models.Model):
    _name = "estate"
    _description = "Bienes Raices"
    _sql_constraints=[
        ('check_expected_price', 'CHECK(expected_price > 0)', 'El precio esperado debe ser un valor mayor a cero.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'El precio de venta no debe ser negativo.'),

    ]

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string="Descripcion")
    postcode = fields.Char(string='Codigo Postal')
    date_availability = fields.Date(string= 'Fecha Disponible', default=lambda self: (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False) #fecha de disponibilidad predeterminada en 3 meses
    expected_price = fields.Float(string='Precio Esperado',required=True)
    selling_price = fields.Float(string= 'Precio de venta', readonly=True, copy=False)
    bedrooms = fields.Integer(string= 'Dormitorios', default=2)
    living_area = fields.Integer(string= 'Area de Sala en (m2)')
    facades = fields.Integer(string= 'Fachadas')
    garage = fields.Boolean(string= 'Cochera')
    garden = fields.Boolean(string='Jardin')
    garden_area = fields.Integer(string= ' Area de jardin en (m2)')
    garden_orientation = fields.Selection([('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'), ('oeste', 'Oeste')], string= 'Orientacion del jardin')
    active = fields.Boolean(string='Activo', default=True)
    state = fields.Selection([('nuevo', 'Nuevo'), ('oferta_recibida', 'Oferta Recibida'), ('oferta_aceptada', 'Oferta Aceptada'), ('vendido', 'Vendido'), ('cancelado', 'Cancelado')], default='nuevo', string= 'Estado', required=True)
    type_id = fields.Many2one('estate_type', string = 'Tipo')
    ven_id = fields.Many2one('res.users', string= 'Nombre del vendedor', default=lambda self:self.env.user)
    com_id = fields.Many2one('res.partner',string='Nombre del comprador', copy=False, compute='_compute_customer', store=True)
    tag_ids = fields.Many2many('estate_tag', string = 'Etiquetas')
    offer_ids = fields.One2many("estate_offer", "property_id", string='Oferta')
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string='best price', compute='_compute_best_price')

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            property_offers = record.offer_ids.mapped("price")
            record.best_price = max(property_offers) if property_offers else 0.0
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    def action_cancel_estate(self):
        for record in self:
            if record.state !='vendido':
                record.state='cancelado'
            else:
                raise exceptions.UserError('No se puede cancelar una propiedad vendida.')

    def action_set_sold(self):
        for record in self:
            if record.state != 'cancelado':
                if record.state == 'vendido':
                    raise exceptions.UserError("No se puede vender una propiedad vendida.")

                else:
                    record.state = 'vendido'

            else:
                raise exceptions.UserError("No se puede vender una propiedad cancelada.")

    @api.depends('offer_ids', 'offer_ids.status', 'offer_ids.partner_id')
    def _compute_customer(self):
        for estate in self:
            accepted_offers = estate.offer_ids.filtered(lambda offer: offer.status == 'aceptado')
            if accepted_offers:
                estate.com_id = accepted_offers[0].partner_id
            else:
                estate.com_id = False