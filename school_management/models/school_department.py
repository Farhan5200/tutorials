# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolDepartment(models.Model):
    """used to create department in school"""
    _name = "school.department"
    _description = "School Department"
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    head_of_department_id = fields.Many2one("res.partner", string="Head", tracking=True)
