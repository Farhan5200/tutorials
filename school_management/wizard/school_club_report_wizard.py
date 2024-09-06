# -*- coding: utf-8 -*-

import html2text
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import json, date_utils
import io
import json
try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter

class SchoolClubReportWizard(models.TransientModel):
    """For club report wizard"""
    _name = "school.club.report.wizard"
    _description = "School Club Report Wizard"

    club_id = fields.Many2many('school.club', string="Club")

    def action_print_report_pdf(self):
        """For printing club report"""
        data = {
            'selected_club': self.club_id.ids
        }


        return self.env.ref('school_management.action_report_school_club').report_action(None, data=data)

    def action_print_report_xlsx(self):
        """to print xlsx report"""
        data = {
            'selected_club': self.club_id.ids
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'school.club.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """to create xlsx report"""
        selected_club = data['selected_club']
        company_details = html2text.html2text(self.env.company.company_details)

        query = """select school_club.id, school_club.name as club_name , student_registration.first_name as student_name,
                 student_registration.name as admission_no, student_registration.gender as gender, school_class.name as 
                 class_name from(((school_club inner join school_club_student_registration_rel on school_club.id =
                 school_club_student_registration_rel.school_club_id) inner join student_registration on
                  student_registration.id = school_club_student_registration_rel.student_registration_id) inner join 
                  school_class on school_class.id = student_registration.current_class_id)"""

        club_query = "select id,name from school_club"

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(club_query)
        club_name = self.env.cr.dictfetchall()

        if club_name:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center'})

            row = 9
            sheet.merge_range('A1:F6', company_details, cell_format)
            sheet.merge_range('B7:I8', 'CLUB REPORT', head)
            if selected_club:
                for selected in selected_club:
                    for all_club in club_name:
                        if selected == all_club['id']:
                            row += 1
                            sheet.merge_range(f'A{row}:H{row}', f'Club Name : {all_club["name"]}', cell_format)
                            row += 1
                            sheet.merge_range(f'A{row}:B{row}', 'Admission Number', cell_format)
                            sheet.merge_range(f'C{row}:D{row}', 'Name', cell_format)
                            sheet.merge_range(f'E{row}:F{row}', 'Class', cell_format)
                            sheet.merge_range(f'G{row}:H{row}', 'Gender', cell_format)
                            for docs in report:
                                if all_club['id'] == docs['id']:
                                    row += 1
                                    sheet.merge_range(f'A{row}:B{row}', docs['admission_no'], txt)
                                    sheet.merge_range(f'C{row}:D{row}', docs['student_name'], txt)
                                    sheet.merge_range(f'E{row}:F{row}', docs['class_name'], txt)
                                    sheet.merge_range(f'G{row}:H{row}', docs['gender'], txt)
                    row += 1
            else:
                for all_club in  club_name:
                    row += 1
                    sheet.merge_range(f'A{row}:H{row}', f'Club Name : {all_club["name"]}', cell_format)
                    row += 1
                    sheet.merge_range(f'A{row}:B{row}', 'Admission Number', cell_format)
                    sheet.merge_range(f'C{row}:D{row}', 'Name', cell_format)
                    sheet.merge_range(f'E{row}:F{row}', 'Class', cell_format)
                    sheet.merge_range(f'G{row}:H{row}', 'Gender', cell_format)
                    for docs in report:
                        if all_club['id'] == docs['id']:
                            row += 1
                            sheet.merge_range(f'A{row}:B{row}', docs['admission_no'], txt)
                            sheet.merge_range(f'C{row}:D{row}', docs['student_name'], txt)
                            sheet.merge_range(f'E{row}:F{row}', docs['class_name'], txt)
                            sheet.merge_range(f'G{row}:H{row}', docs['gender'], txt)
                    row += 1
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            raise ValidationError('No records.....!')

