from odoo import models, fields


class Patient(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer("Age")
    date_of_birth = fields.Date("Date Of Birth")
    blood_group = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], string="Blood Group")
