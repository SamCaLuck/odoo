from odoo import models, fields

class Estate_type(models.Model):
    _name = 'estate_type'
    _description = 'Tipo de propiedad'
    _sql_constraints = [
        ('check_type', 'UNIQUE(name)', 'El nombre debe ser unico')
    ]
    name = fields.Char(string='Tipo de propiedad', required=True)