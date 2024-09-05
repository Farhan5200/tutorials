# -*- coding: utf-8 -*-

from odoo import api, fields,models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class SchoolLeaveReportWizard(models.TransientModel):
    _name = "school.leave.report.wizard"
    _description = "School Leave Report Wizard"

    interval = fields.Selection([
        ('this_month', 'This Month'),
        ('this_week', 'This Week'),
        ('this_day', 'This Day'),
        ('custom', 'Custom')
    ], string="Interval", default="custom", required=True)

    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")
    class_id = fields.Many2one('school.class', string="Class")
    student_id = fields.Many2one('student.registration', domain="[('current_class_id', '=', class_id)]", string="Student")
    student_domain_ids = fields.Many2many('student.registration', compute='_compute_student_domain_ids')



    @api.depends('class_id')
    def _compute_student_domain_ids(self):
        for rec in self:
            if rec.class_id:
                rec.student_domain_ids = rec.env['student.registration'].search([('current_class_id', '=', rec.class_id.id)])
            else:
                rec.student_domain_ids = rec.env['student.registration'].search([])

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.student_id = False

    def action_print_report(self):
        data={
            'select_student_name': self.student_id.first_name,
            'select_class_name': self.class_id.name,
            'interval': self.interval,
            'from_date': self.from_date,
            'to_date': self.to_date
        }

        return self.env.ref('school_management.action_report_school_leave').report_action(None, data=data)

