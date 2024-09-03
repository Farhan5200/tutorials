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
        ('this_year', 'This Year'),
        ('this_week', 'This Week'),
        ('custom', 'Custom')
    ], string="Start Date")

    def action_print_report(self):
        data = {
            'select_club_name': self.club_id.name,
            'event_start_date': self.event_start_date,
            'from_date': self.from_date,
            'to_date': self.to_date

        }
        return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)


class AllEventReport(models.AbstractModel):
    _name = "report.school_management.report_event"
    _description = "All event report"

    @api.model
    def _get_report_values(self, docids, data=None):
        select_club_name = data['select_club_name']
        event_start_date = data['event_start_date']
        from_date = data['from_date']
        to_date = data['to_date']

        query = """select school_event.id,school_event.name as event_name,school_event.start_date,
        school_event.end_date,school_event.status,school_club.name as club_name from 
        ((school_event inner join school_club_school_event_rel on school_event.id = 
        school_club_school_event_rel.school_event_id)inner join school_club on 
        school_club.id = school_club_school_event_rel.school_club_id)"""
        if select_club_name and event_start_date == 'custom':
            query += " where school_club.name = '%s'" %select_club_name
            query += " and school_event.start_date >= '%s'" % from_date
            query += " and school_event.start_date <= '%s'" % to_date
        if event_start_date == 'custom' and not select_club_name:
            query += " where school_event.start_date >= '%s'" % from_date
            query += " and school_event.start_date <= '%s'" % to_date
        if select_club_name and not event_start_date:
            query += " where school_club.name = '%s'" %select_club_name

        print(query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        return {
            'docs': report
        }

