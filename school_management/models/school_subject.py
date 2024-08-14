# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolSubject(models.Model):
    """used to create subjects available in school"""
    _name = "school.subject"
    _description = "School Subject"
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    subject_department_id = fields.Many2many("school.department", string="Department", tracking=True)
