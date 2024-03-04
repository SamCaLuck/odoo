from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
class EstateOffer(models.Model):
    _name = 'estate_offer'
    _description = 'oferta'
    _sql_constraints = [
        ('check_offer_ids', 'CHECK(price > 0)', 'El precio de oferta debe ser positivo y mayor a cero.')
    ]

    price = fields.Float(string='precio')
    status = fields.Selection([('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], string='estado', copy=False)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    property_id = fields.Many2one('estate', required=True)

    validity = fields.Integer(default=7, string='Validez')
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Expira')

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days


    def action_accept_offer(self):

        if 'aceptado' in self.mapped('property_id.offer_ids.status'):
            raise UserError('Ya existe una oferta aceptada.')
                # continue  # Si ya está aceptado, no hagas nada
        self.write({'status': 'aceptado'})
            # property_record = record.property_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'oferta_aceptada'

    def action_refuse_offer(self):
        return self.write(
            {
                'status': 'rechazado'
            }
        )

    def unlink(self):
        for record in self:
            if record.status == 'aceptado':
                property_record = record.property_id
                property_record.selling_price -= record.price
        return super(EstateOffer, self).unlink()