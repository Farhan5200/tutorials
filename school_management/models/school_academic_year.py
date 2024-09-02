# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolAcademicYear(models.Model):
    """used to create Academic year"""
    _name = 'school.academic.year'
    _description = 'School Academic Year'
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    start_date = fields.Date("Start Date", required=True, tracking=True)
    end_date = fields.Date("End Date", required=True, tracking=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """to check if the start date is greater than end date"""
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.start_date > rec.end_date:
                    raise ValidationError("Start date is greater than end date")
