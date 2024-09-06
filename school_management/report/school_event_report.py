# -*- coding: utf-8 -*-


from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class SchoolEventReport(models.AbstractModel):
    """For passing values to the event report"""

    _name = "report.school_management.report_event"
    _description = "All event report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """For passing values to the event pdf report"""

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
