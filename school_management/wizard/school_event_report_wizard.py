# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from odoo.tools import date_utils


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


class AllEventReport(models.AbstractModel):
    _name = "report.school_management.report_event"
    _description = "All event report"

    @api.model
    def _get_report_values(self, docids, data=None):
        select_club_name = data['select_club_name']
        event_start_date = data['event_start_date']
        from_date = data['from_date']
        to_date = data['to_date']
        today = fields.Date.today()
        report_type = {'report_type': 'Complete Report',
                       'event_start_date': event_start_date}

        query = """select school_event.id,school_event.name as event_name,school_event.start_date,
        school_event.end_date,school_event.status,school_club.name as club_name from 
        ((school_event inner join school_club_school_event_rel on school_event.id = 
        school_club_school_event_rel.school_event_id)inner join school_club on 
        school_club.id = school_club_school_event_rel.school_club_id)"""

        if event_start_date == 'this_month':
            from_date = date_utils.start_of(today, "month")
            to_date = date_utils.end_of(today, "month")
            report_type['report_type'] = 'This Month Report'

        if event_start_date == 'this_week':
            from_date = date_utils.start_of(today, "week")
            to_date = date_utils.end_of(today, "week")
            report_type['report_type'] = 'This Week Report'

        if event_start_date == 'this_day':
            from_date = today
            to_date = today
            report_type['report_type'] = 'Today Report'

        if select_club_name and event_start_date:
            if event_start_date != 'custom':
                query += """ where school_club.name = '%s'and school_event.start_date >=
                 '%s'and school_event.start_date <= '%s'""" % (select_club_name, from_date, to_date)
            elif from_date and not to_date:
                query += " where school_club.name = '%s' and school_event.start_date >='%s'" %(select_club_name,from_date)
            elif to_date and not from_date:
                query += " where school_club.name = '%s' and school_event.start_date <= '%s'" %(select_club_name,to_date)
            elif from_date and to_date:
                query += """ where school_club.name = '%s' and school_event.start_date >= '%s' and 
                school_event.start_date <= '%s'""" % (select_club_name,from_date, to_date)
            elif not from_date and not to_date:
                query += " where school_club.name = '%s'" %select_club_name

        if event_start_date and not select_club_name:
            if event_start_date != 'custom':
                query += " where school_event.start_date >= '%s' and school_event.start_date <= '%s'" % (from_date, to_date)
            elif from_date and not to_date:
                query += " where school_event.start_date >='%s'" %from_date
            elif to_date and not from_date:
                query += " where school_event.start_date <= '%s'" %to_date
            elif from_date and to_date:
                query += " where school_event.start_date >= '%s' and school_event.start_date <= '%s'" % (
                from_date, to_date)

        if select_club_name and not event_start_date:
            query += " where school_club.name = '%s'" %select_club_name

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        dates ={
            'from_date': from_date,
            'to_date': to_date,
            'current_date': today
        }
        if report:
            remove_duplicate = []
            unique_event = []
            for i in report:
                if i['id'] not in remove_duplicate:
                    remove_duplicate.append(i['id'])
                    unique_event.append(i)

            return {
                'docs': unique_event,
                'all_club': report,
                'report_type': report_type,
                'dates': dates
            }
        else:
            raise ValidationError('There are no records matching your condition')

