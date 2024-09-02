# -*- coding: utf-8 -*-

from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError

class SchoolExam(models.Model):
    _name = "school.exam"
    _description = "School Exam"

    name = fields.Char(string="Name", required=True)
    class_id = fields.Many2one("school.class", string="Class")
    paper_ids = fields.One2many("school.exam.paper", inverse_name="exam_id")
    exam_assigned_student_ids = fields.Many2many("student.registration", domain="[('status', '=', 'registration')]")
    start_date = fields.Date(strint="Start date")
    end_date = fields.Date(string="End date")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('announced', 'Announced'),
        ('canceled', 'Canceled'),
        ('done', 'Done')
    ], default="draft")
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company)
    active = fields.Boolean(default=True)
    hide_button = fields.Boolean(default=False)


    def action_button_assign(self):
        """for assigning exams to all students"""
        for rec in self:
            temp = self.env["student.registration"].search([('status', '=', 'registration'),('current_class_id.id', '=', rec.class_id.id)])
            rec.exam_assigned_student_ids = [Command.set(temp.ids)]
            rec.hide_button = True

    def action_button_cancel(self):
        """for changing status to cancel"""
        self.status = 'canceled'

    def action_button_announce(self):
        """for changing status to announce"""
        self.status = 'announced'

    def archive_completed_exam_action(self):
        """scheduled action : if exam end date is past this function will set the status of the
                event to done and archives the event"""
        all_exams = self.search([])
        for rec in all_exams:
            if rec.end_date < fields.Date.today():
                rec.active = False
                rec.status = "done"

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """to check if the start date is greater than end date"""
        for rec in self:
            if (rec.start_date and rec.end_date) and (rec.start_date > rec.end_date):
                raise ValidationError("Start date is greater than end date")
