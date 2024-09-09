# -*- coding: utf-8 -*-

import html2text
from odoo import api, fields,models
from odoo.exceptions import ValidationError
from odoo.tools import json, date_utils
import io
try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


class SchoolLeaveReportWizard(models.TransientModel):
    """For leave report wizard"""

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

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        """to check if the from date is greater than to date"""
        for rec in self:
            if (rec.from_date and rec.to_date) and (rec.from_date > rec.to_date):
                raise ValidationError("From date is greater than to date")



    @api.depends('class_id')
    def _compute_student_domain_ids(self):
        """Dynamic domain for student_id"""
        for rec in self:
            if rec.class_id:
                rec.student_domain_ids = rec.env['student.registration'].search([('current_class_id', '=', rec.class_id.id)])
            else:
                rec.student_domain_ids = rec.env['student.registration'].search([])

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.student_id = False

    @api.onchange('interval')
    def _onchange_interval(self):
        self.from_date = False
        self.to_date = False

    def action_print_report_pdf(self):
        """For printing leave report"""

        data={
            'select_student_name': self.student_id.first_name,
            'select_class_name': self.class_id.name,
            'interval': self.interval,
            'from_date': self.from_date,
            'to_date': self.to_date
        }

        return self.env.ref('school_management.action_report_school_leave').report_action(None, data=data)

    def action_print_report_xlsx(self):
        """to print xlsx report"""
        data = {
            'select_student_name': self.student_id.first_name,
            'select_class_name': self.class_id.name,
            'interval': self.interval,
            'from_date': self.from_date,
            'to_date': self.to_date
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'school.leave.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }
    def get_xlsx_report(self, data, response):
        """to create xlsx report"""
        select_student_name = data['select_student_name']
        select_class_name = data['select_class_name']
        interval = data['interval']
        from_date = data['from_date'] or None
        to_date = data['to_date'] or None
        today = fields.Date.today()
        report_type = {'report_type': 'Complete Report',
                       'interval': interval}
        company_details = html2text.html2text(self.env.company.company_details)


        query = """select student_registration.first_name as student_name, school_class.name as class_name, 
                school_leaves.start_date, school_leaves.end_date, school_leaves.reason, school_leaves.total_days as duration, 
                school_leaves.half_day, school_leaves.fn_or_an from((school_leaves inner join student_registration on 
                student_registration.id =  school_leaves.student_id) inner join school_class on school_class.id = 
                student_registration.current_class_id)"""

        if interval == 'this_month':
            from_date = date_utils.start_of(today, "month")
            to_date = date_utils.end_of(today, "month")
            report_type['report_type'] = 'This Month Report'

        if interval == 'this_week':
            from_date = date_utils.start_of(today, "week")
            to_date = date_utils.end_of(today, "week")
            report_type['report_type'] = 'This Week Report'

        if interval == 'this_day':
            from_date = today
            to_date = today
            report_type['report_type'] = 'Today Report'

        if select_class_name and interval and not select_student_name:
            if interval != 'custom':
                query += """ where school_class.name = '%s'and school_leaves.start_date >=
                         '%s'and school_leaves.start_date <= '%s'""" % (select_class_name, from_date, to_date)
            elif from_date and not to_date:
                query += " where school_class.name = '%s' and school_leaves.start_date >='%s'" % (
                select_class_name, from_date)
            elif to_date and not from_date:
                query += " where school_class.name = '%s' and school_leaves.start_date <= '%s'" % (
                select_class_name, to_date)
            elif from_date and to_date:
                query += """ where school_class.name = '%s' and school_leaves.start_date >= '%s' and 
                                        school_leaves.start_date <= '%s'""" % (select_class_name, from_date, to_date)
            elif not from_date and not to_date:
                query += " where school_class.name = '%s'" % select_class_name

        if interval and not select_class_name and not select_student_name:
            if interval != 'custom':
                query += " where school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'" % (
                from_date, to_date)
            elif from_date and not to_date:
                query += " where school_leaves.start_date >='%s'" % from_date
            elif to_date and not from_date:
                query += " where school_leaves.start_date <= '%s'" % to_date
            elif from_date and to_date:
                query += " where school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'" % (
                    from_date, to_date)

        if select_class_name and not interval and not select_student_name:
            query += " where school_class.name = '%s'" % select_class_name

        if select_class_name and select_student_name and interval:
            if interval != 'custom':
                query += (""" where school_class.name = '%s' and student_registration.first_name = '%s' and 
                        school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'"""
                          % (select_class_name, select_student_name, from_date, to_date))
            elif from_date and not to_date:
                query += """where school_class.name = '%s' and student_registration.first_name = '%s' and 
                        school_leaves.start_date >= '%s'""" % (select_class_name, select_student_name, from_date)
            elif to_date and not from_date:
                query += """where school_class.name = '%s' and student_registration.first_name = '%s' and 
                        school_leaves.start_date <= '%s'""" % (select_class_name, select_student_name, to_date)
            elif from_date and to_date:
                query += (""" where school_class.name = '%s' and student_registration.first_name = '%s' and 
                                        school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'"""
                          % (select_class_name, select_student_name, from_date, to_date))
            elif not from_date and not to_date:
                query += ("""where school_class.name = '%s' and student_registration.first_name = '%s'"""
                          % (select_class_name, select_student_name))

        if select_class_name and select_student_name and not interval:
            query += (""" where school_class.name = '%s' and student_registration.first_name = '%s'"""
                      % (select_class_name, select_student_name))

        if not select_class_name and select_student_name and interval:
            if interval != "custom":
                query += """ where student_registration.first_name = '%s' and school_leaves.start_date >= '%s' 
                        and school_leaves.start_date <= '%s'""" % (select_student_name, from_date, to_date)
            elif from_date and not to_date:
                query += (""" where student_registration.first_name = '%s' and school_leaves.start_date >= '%s'"""
                          % (select_student_name, from_date))
            elif to_date and not from_date:
                query += (""" where student_registration.first_name = '%s' and school_leaves.start_date <= '%s'"""
                          % (select_student_name, to_date))
            elif from_date and to_date:
                query += """ where student_registration.first_name = '%s' and school_leaves.start_date >= '%s' 
                                        and school_leaves.start_date <= '%s'""" % (
                select_student_name, from_date, to_date)
            elif not from_date and not to_date:
                query += """ where student_registration.first_name = '%s'""" % select_student_name

        if not select_class_name and select_student_name and not interval:
            query += """ where student_registration.first_name = '%s'""" % select_student_name

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        if report:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '10px', 'align': 'center', 'bold': True, 'border':1})
            top_head = workbook.add_format(
                {'font_size': '10px', 'align': 'center', 'bold': True})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center', 'border':1})

            sheet.merge_range('A1:N6', company_details, cell_format)
            sheet.merge_range('A7:N8', 'LEAVE REPORT', head)
            sheet.merge_range('A10:D10', f'Report Type : {report_type["report_type"]}', top_head)
            if from_date and to_date:
                sheet.merge_range('A11:D11', f'From Date : {str(from_date)}', top_head)
                sheet.merge_range('F11:H11', f'To Date : {str(to_date)}', top_head)
            elif from_date and not to_date:
                sheet.merge_range('A11:D11', f'From Date : {str(from_date)}', top_head)
            elif not from_date and to_date:
                sheet.merge_range('A11:D11', f'Upto : {str(to_date)}', top_head)



            # Heading
            sheet.merge_range('A13:B13', 'Student', cell_format)
            sheet.merge_range('C13:D13', 'Class', cell_format)
            sheet.merge_range('E13:F13', 'Start Date', cell_format)
            sheet.merge_range('G13:H13', 'End Date', cell_format)
            sheet.write('I13', 'Days', cell_format)
            sheet.write('J13', 'FN/AN', cell_format)
            sheet.merge_range('K13:N13', 'Reason', cell_format)

            # Body
            row = 13
            for rec in report:
                row += 1
                sheet.merge_range(f'A{row}:B{row}', rec['student_name'], txt)
                sheet.merge_range(f'C{row}:D{row}', rec['class_name'], txt)
                sheet.merge_range(f'E{row}:F{row}', str(rec['start_date']), txt)
                sheet.merge_range(f'G{row}:H{row}', str(rec['end_date']), txt)
                sheet.write(f'I{row}', rec['duration'], txt)
                if rec['half_day']:
                    if rec['fn_or_an'] == 'fn':
                        sheet.write(f'J{row}', 'FN', txt)
                    if rec['fn_or_an'] == 'an':
                        sheet.write(f'J{row}', 'AN', txt)
                else:
                    sheet.write(f'J{row}', 'Full day', txt)
                sheet.merge_range(f'K{row}:N{row}', rec['reason'], txt)

            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            raise ValidationError('There are no records matching your condition')



