# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    employee_type = fields.Selection([
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('office staff', 'Office Staff')
    ], string="Employee Type")
    email = fields.Char(copy=False)

    _sql_constraints = [
        ('email_unique', 'unique(email)', "This email is already exists")]
