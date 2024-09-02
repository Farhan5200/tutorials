# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolClass(models.Model):
    """used to create multiple classes in school"""
    _name = "school.class"
    _description = "School Class"
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    department_id = fields.Many2one("school.department", string="Department", tracking=True)
    head_of_department_id = fields.Many2one('res.partner', string="Head", tracking=True,
                                            related="department_id.head_of_department_id", readonly=False)
    school_id = fields.Many2one("res.company", string="School", tracking=True, default=lambda self: self.env.company)
    student_ids = fields.One2many("student.registration",inverse_name="current_class_id")
