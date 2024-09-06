# -*- coding: utf-8 -*-

import html2text
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
import io
import json
try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


class SchoolEventReportWizard(models.TransientModel):
    """For event report wizard"""

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

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        """to check if the from date is greater than to date"""
        for rec in self:
            if (rec.from_date and rec.to_date) and (rec.from_date > rec.to_date):
                raise ValidationError("From date is greater than to date")

    @api.onchange('event_start_date')
    def _onchange_event_start_date(self):
        self.from_date = False
        self.to_date = False

    def action_print_report_pdf(self):
        """For printing event report"""

        data = {
            'select_club_name': self.club_id.name,
            'event_start_date': self.event_start_date,
            'from_date': self.from_date,
            'to_date': self.to_date

        }
        return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)

    def action_print_report_xlsx(self):
        """to print xlsx report"""
        data = {
            'select_club_name': self.club_id.name,
            'event_start_date': self.event_start_date,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'state': dict(self.env['school.event']._fields['status'].selection)
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'school.event.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }


    def get_xlsx_report(self, data, response):
        """to create xlsx report"""

        select_club_name = data['select_club_name']
        event_start_date = data['event_start_date']
        from_date = data['from_date'] or None
        to_date = data['to_date'] or None
        today = fields.Date.today()
        report_type = {'report_type': 'Complete Report',
                       'event_start_date': event_start_date}
        state = data['state']
        company_details = html2text.html2text(self.env.company.company_details)


        query = """select school_event.id,school_event.name as event_name,school_event.start_date,
               school_event.end_date,school_event.status,school_club.name as club_name from 
               ((school_event inner join school_club_school_event_rel on school_event.id = 
               school_club_school_event_rel.school_event_id)inner join school_club on 
               school_club.id = school_club_school_event_rel.school_club_id)"""

        if event_start_date == 'this_month':
            from_date = str(date_utils.start_of(today, "month"))
            to_date = str(date_utils.end_of(today, "month"))
            report_type['report_type'] = 'This Month Report'

        if event_start_date == 'this_week':
            from_date = str(date_utils.start_of(today, "week"))
            to_date = str(date_utils.end_of(today, "week"))
            report_type['report_type'] = 'This Week Report'

        if event_start_date == 'this_day':
            from_date = str(today)
            to_date = str(today)
            report_type['report_type'] = 'Today Report'

        if select_club_name and event_start_date:
            if event_start_date != 'custom':
                query += """ where school_club.name = '%s'and school_event.start_date >=
                        '%s'and school_event.start_date <= '%s'""" % (select_club_name, from_date, to_date)
            elif from_date and not to_date:
                query += " where school_club.name = '%s' and school_event.start_date >='%s'" % (
                select_club_name, from_date)
            elif to_date and not from_date:
                query += " where school_club.name = '%s' and school_event.start_date <= '%s'" % (
                select_club_name, to_date)
            elif from_date and to_date:
                query += """ where school_club.name = '%s' and school_event.start_date >= '%s' and 
                       school_event.start_date <= '%s'""" % (select_club_name, from_date, to_date)
            elif not from_date and not to_date:
                query += " where school_club.name = '%s'" % select_club_name

        if event_start_date and not select_club_name:
            if event_start_date != 'custom':
                query += " where school_event.start_date >= '%s' and school_event.start_date <= '%s'" % (
                from_date, to_date)
            elif from_date and not to_date:
                query += " where school_event.start_date >='%s'" % from_date
            elif to_date and not from_date:
                query += " where school_event.start_date <= '%s'" % to_date
            elif from_date and to_date:
                query += " where school_event.start_date >= '%s' and school_event.start_date <= '%s'" % (
                    from_date, to_date)

        if select_club_name and not event_start_date:
            query += " where school_club.name = '%s'" % select_club_name

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        if report:
            remove_duplicate = []
            unique_event = []
            for rec in report:
                if rec['id'] not in remove_duplicate:
                    remove_duplicate.append(rec['id'])
                    unique_event.append(rec)

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center'})

            sheet.merge_range('A1:F6', company_details, cell_format)
            sheet.merge_range('B7:I8', 'EVENT REPORT', head)
            sheet.merge_range('A10:B10', 'Report Type: ', cell_format)
            sheet.merge_range('C10:D10', report_type['report_type'], cell_format)
            sheet.merge_range('A11:B11', 'From Date:', cell_format)
            sheet.merge_range('C11:D11', from_date, txt)
            sheet.write('F11', 'To Date:', cell_format)
            sheet.merge_range('G11:H11', to_date, txt)

            # Heading
            sheet.merge_range('A13:B13', 'Name', cell_format)
            sheet.merge_range('C13:D13', 'Start Date', cell_format)
            sheet.merge_range('E13:F13', 'End Date', cell_format)
            sheet.merge_range('G13:H13', 'Club', cell_format)
            sheet.merge_range('I13:J13', 'Status', cell_format)

            # Body
            row = 13
            for event in unique_event:
                clubs = ""
                row += 1
                sheet.merge_range(f'A{row}:B{row}', event['event_name'], txt)
                sheet.merge_range(f'C{row}:D{row}', str(event['start_date']), txt)
                sheet.merge_range(f'E{row}:F{row}', str(event['end_date']), txt)
                clubs = ', '.join(club['club_name'] for club in report if club['id'] == event['id'])
                sheet.merge_range(f'G{row}:H{row}', clubs, txt)
                sheet.merge_range(f'I{row}:J{row}', state[event['status']], txt)
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            raise ValidationError('There are no records matching your condition')




