from odoo import models, fields

class EstateTag(models.Model):
    _name = 'estate_tag'
    _description = 'Etiqueta de propiedad'
    _sql_constraints = [
        ('check_tag', 'UNIQUE(name)', 'El nombre de la etiqueta debe ser unico')
    ]
    name = fields.  Char(string='Etiqueta de propiedad', required=True)
