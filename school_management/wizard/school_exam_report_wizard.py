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

class SchoolExamReportWizard(models.TransientModel):
    """For exam report wizard"""

    _name = "school.exam.report.wizard"
    _description = "School Exam Report Wizard"

    exam_id = fields.Many2one('school.exam', string="Exam")
    class_id = fields.Many2one('school.class', string="Class")
    exam_domain_ids = fields.Many2many('school.exam', compute="_compute_exam_domain_ids")


    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.exam_id = False

    @api.depends('class_id')
    def _compute_exam_domain_ids(self):
        """Dynamic domain for exam_id"""
        for rec in self:
            if not rec.class_id:
                rec.exam_domain_ids = rec.env['school.exam'].search([])
            else:
                rec.exam_domain_ids = rec.env['school.exam'].search([('class_id', '=', rec.class_id.id)])




    def action_print_report_pdf(self):
        """For printing exam report"""

        data={
            'class_name': self.class_id.name,
            'exam_name': self.exam_id.name
        }

        return self.env.ref('school_management.action_report_school_exam').report_action(None, data=data)

    def action_print_report_xlsx(self):
        """for printing xlsx report"""
        data = {
            'class_name': self.class_id.name,
            'exam_name': self.exam_id.name
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'school.exam.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """to create xlsx report"""
        class_name = data['class_name']
        exam_name = data['exam_name']
        company_details = html2text.html2text(self.env.company.company_details)


        exam_query = """select school_exam.name as exam_name, school_exam.start_date as start_date, school_exam.end_date as 
                end_date, school_class.name as class_name from(school_exam inner join school_class on school_exam.class_id = 
                school_class.id)"""

        paper_query = """select school_subject.name as exam_paper, school_exam_paper.pass_mark, school_exam_paper.max_mark,
                 school_exam.name as exam_name from (school_exam_paper inner join school_subject on school_subject.id = 
                 school_exam_paper.subject_id) inner join school_exam on school_exam.id = school_exam_paper.exam_id"""

        if class_name and not exam_name:
            exam_query += " where school_class.name = '%s'" % class_name
        if exam_name and not class_name:
            exam_query += " where school_exam.name = '%s'" % exam_name
        if exam_name and class_name:
            exam_query += " where school_class.name = '%s' and school_exam.name = '%s'" % (class_name, exam_name)

        self.env.cr.execute(exam_query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(paper_query)
        paper = self.env.cr.dictfetchall()

        if report:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center', 'border':1, 'bold':True})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center', 'border':1})
            side = workbook.add_format({'font_size': '10px','bold':True})


            sheet.merge_range('A1:F6', company_details, cell_format)
            sheet.merge_range('A7:F8', 'EXAM REPORT', head)
            row = 9
            for rec in report:
                row += 1
                sheet.merge_range(f'A{row}:F{row}', f'Class : {rec["class_name"]}', side)
                row += 1
                sheet.merge_range(f'A{row}:F{row}', f'Exam Name : {rec["exam_name"]}', side)
                row += 1
                sheet.merge_range(f'A{row}:F{row}', f'Start Date : {rec["start_date"]}', side)
                row += 1
                sheet.merge_range(f'A{row}:F{row}', f'End Date : {rec["end_date"]}', side)
                row += 1
                sheet.merge_range(f'A{row}:B{row}', 'Paper', cell_format)
                sheet.merge_range(f'C{row}:D{row}', 'Pass Mark', cell_format)
                sheet.merge_range(f'E{row}:F{row}', 'Max Mark', cell_format)
                for pap in paper:
                    if rec['exam_name'] == pap['exam_name']:
                        row += 1
                        sheet.merge_range(f'A{row}:B{row}', pap['exam_paper'], txt)
                        sheet.merge_range(f'C{row}:D{row}', pap['pass_mark'], txt)
                        sheet.merge_range(f'E{row}:F{row}', pap['max_mark'], txt)
                row += 2


            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            raise ValidationError('No records.....!')





