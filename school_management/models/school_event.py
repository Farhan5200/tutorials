# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SchoolEvent(models.Model):
    """to create event creation form"""
    _name = "school.event"
    _description = "School Event"
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    club_ids = fields.Many2many("school.club", required=True)
    photo = fields.Image("Photo")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('announced', 'Announced'),
        ('canceled', 'Canceled'),
        ('done', 'Done')],
        tracking=True, default="draft", copy=False
    )
    description = fields.Html()
    active = fields.Boolean(default=True)
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company)

    @api.onchange('status')
    def _onchange_status(self):
        """to archive events in done stage"""
        for rec in self:
            if rec.status == 'done':
                rec.active = False
            else:
                rec.active = True

    def archive_completed_events_action(self):
        """scheduled action : if event end date is past this function will set the status of the
        event to done and archives the event"""
        all_events = self.search([])
        for rec in all_events:
            if rec.end_date < fields.Date.today():
                rec.status = 'done'
                rec.active = False

    def send_event_reminder_email(self):
        """scheduled action : send reminder email to all employees on 2 days before start date of the event"""
        mail_template = self.env.ref('school_management.event_email_template')
        receipts_mail = ','.join(rec.email for rec in self.env['res.partner'].search([('employee_type', '!=', False)]))
        all_events = self.search([])
        for rec in all_events:
            schedule_date = rec.start_date - timedelta(days=2)
            if fields.Date.today() == schedule_date:
                email_vals = {
                    'email_to': receipts_mail
                }
                mail_template.send_mail(rec.id, email_values=email_vals, force_send=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """to check if the start date is greater than end date"""
        for rec in self:
            if (rec.start_date and rec.end_date) and (rec.start_date > rec.end_date):
                raise ValidationError("Start date is greater than end date")
