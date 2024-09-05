# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SchoolEventReportWizard(models.TransientModel):
    _name = "school.event.report.wizard"
    _description = "School Event Report Wizard"

    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")
    club_id = fields.Many2one('school.club', string="Club")
    event_start_date = fields.Selection([
        ('this_month', 'This Month'),
        ('this_week', 'This Week'),
        ('this_day', 'This Day'),
        ('custom', 'Custom')
    ], string="Interval", default="custom", required=True)

    def action_print_report(self):
        data = {
            'select_club_name': self.club_id.name,
            'event_start_date': self.event_start_date,
            'from_date': self.from_date,
            'to_date': self.to_date

        }
        return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)


