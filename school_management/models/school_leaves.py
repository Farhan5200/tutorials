# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SchoolLeaves(models.Model):
    _name = "school.leaves"
    _description = "School Leaves"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", invisible=True, default="Leave")
    student_id = fields.Many2one("student.registration", string="Student", required=True,
                                 tracking=True, ondelete='cascade')
    class_id = fields.Many2one("school.class", string="Class", related="student_id.current_class_id")
    start_date = fields.Date(string="Start date", required=True)
    end_date = fields.Date(string="End date", store=True, compute="_compute_end_date")
    total_days = fields.Float(string="Total days", compute="_compute_total_days", store=True)
    half_day = fields.Boolean(string="Half day")
    reason = fields.Text(string="Reason", required=True)
    fn_or_an = fields.Selection([
        ('fn', 'FN'),
        ('an', 'AN')
    ], String="FN/AN")
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company)

    @api.depends('start_date', 'end_date', 'half_day')
    def _compute_total_days(self):
        """to compute total leave days"""
        for rec in self:
            rec.total_days = 0
            if rec.start_date and rec.end_date:
                start_date = rec.start_date
                if start_date > rec.end_date and not rec.half_day:
                    rec.total_days = 0
                    raise ValidationError("Start date is greater than end date...!")
                else:
                    while start_date <= rec.end_date:
                        if start_date.weekday() not in [5, 6]:
                            rec.total_days += 1
                        start_date += timedelta(days=1)

    @api.depends('half_day', 'start_date')
    def _compute_end_date(self):
        """to set end date and total days when checking the boolean half day"""
        for rec in self:
            if rec.half_day and rec.start_date:
                rec.end_date = rec.start_date
                rec.total_days = 0.5
