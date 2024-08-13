# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolAcademicYear(models.Model):
    """used to create Academic year"""
    _name = 'school.academic.year'
    _description = 'School Academic Year'
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    start_date = fields.Date("Start Date", required=True, tracking=True)
    end_date = fields.Date("End Date", required=True, tracking=True)
