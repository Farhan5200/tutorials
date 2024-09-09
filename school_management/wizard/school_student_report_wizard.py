# -*- coding: utf-8 -*-

import html2text
from odoo import api, fields,models
import io
import json

from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


class SchoolStudentReportWizard(models.TransientModel):
    """For student report wizard"""

    _name = "school.student.report.wizard"
    _description = "School Student Report Wizard"

    department_id = fields.Many2one('school.department', string="Department")
    class_id = fields.Many2one('school.class', string="Class")
    class_domain_ids = fields.Many2many('school.class', compute="_compute_department_id_class_id")
    student_id = fields.Many2one('student.registration', string="Student")
    student_domain_ids = fields.Many2many('student.registration', compute='_compute_department_id_class_id')

    @api.depends('department_id', 'class_id')
    def _compute_department_id_class_id(self):
        """Dynamic domain for student_id and class_id"""
        for rec in self:
            if not rec.department_id:
                rec.class_domain_ids = rec.env['school.class'].search([])
                rec.student_domain_ids = rec.env['student.registration'].search([])
            else:
                rec.class_domain_ids = rec.env['school.class'].search([('department_id', '=', rec.department_id.id)])
                rec.student_domain_ids = rec.env['student.registration'].search([('current_class_id.department_id', '=', rec.department_id.id)])
            if self.class_id:
                rec.student_domain_ids = rec.env['student.registration'].search([('current_class_id', '=', rec.class_id.id)])

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.class_id = False
        self.student_id = False

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.student_id = False


    def action_print_report_pdf(self):
        """For printing student report"""

        data={
            'class_name': self.class_id.name,
            'department_name': self.department_id.name,
            'student_name': self.student_id.first_name
        }

        return self.env.ref('school_management.action_report_school_student').report_action(None, data=data)

    def action_print_report_xlsx(self):
        """to print xlsx report"""
        data = {
            'class_name': self.class_id.name,
            'department_name': self.department_id.name,
            'student_name': self.student_id.first_name
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'school.student.report.wizard',
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
        department_name = data['department_name']
        student_name = data['student_name']
        selected_values = {
            'selected_class': class_name,
            'selected_department': department_name,
            'selected_student': student_name
        }
        company_details = html2text.html2text(self.env.company.company_details)

        query = """select student_registration.name as admission_no, student_registration.first_name as name,school_department.id as department_id, 
                school_class.name as class_name, school_department.name as department_name, student_registration.gender as 
                gender from((student_registration inner join school_class on school_class.id = 
                student_registration.current_class_id)inner join school_department on school_class.department_id = 
                school_department.id)"""

        department_query = "select id as dep_id, name as dept_name from school_department"

        class_query = "select name as class_name, id as class_id, department_id from school_class"

        if class_name and department_name:
            if student_name:
                query += " where student_registration.first_name = '%s'" % student_name
            else:
                query += " where school_class.name = '%s' and school_department.name = '%s'" % (
                class_name, department_name)
        if class_name and not department_name:
            if student_name:
                query += " where student_registration.first_name = '%s'" % student_name
            else:
                query += " where school_class.name = '%s'" % class_name
        if not class_name and department_name:
            if student_name:
                query += " where student_registration.first_name = '%s'" % student_name
            else:
                query += " where school_department.name = '%s'" % department_name
        if not class_name and not department_name and student_name:
            query += " where student_registration.first_name = '%s'" % student_name

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(department_query)
        department_details = self.env.cr.dictfetchall()
        self.env.cr.execute(class_query)
        class_details = self.env.cr.dictfetchall()

        if report:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '10px', 'bold':True, 'align': 'center', 'border':1})
            top_txt = workbook.add_format(
                {'font_size': '12px', 'bold':True, 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center', 'border':1})

            sheet.merge_range('A1:F6', company_details, cell_format)
            sheet.merge_range('A7:F8', 'STUDENT REPORT', head)

            if student_name:
                # Heading
                sheet.merge_range('A10:B10', 'Admission Number', cell_format)
                sheet.merge_range('C10:D10', 'Name', cell_format)
                sheet.merge_range('E10:F10', 'Gender', cell_format)
                sheet.write('G10', 'Class', cell_format)
                sheet.merge_range('H10:I10', 'Department', cell_format)

                # Body
                row = 10
                for rec in report:
                    row += 1
                    sheet.merge_range(f'A{row}:B{row}', rec['admission_no'], txt)
                    sheet.merge_range(f'C{row}:D{row}', rec['name'], txt)
                    sheet.merge_range(f'E{row}:F{row}', rec['gender'], txt)
                    sheet.write(f'G{row}', rec['class_name'], txt)
                    sheet.merge_range(f'H{row}:I{row}', rec['department_name'], txt)

            elif department_name and class_name:
                # Head
                sheet.merge_range('A10:C10', f'Department Name : {department_name}', top_txt)
                sheet.merge_range('A11:C11', f'Class Name : {class_name}', top_txt)
                sheet.merge_range('A13:B13', 'Admission Number', cell_format)
                sheet.merge_range('C13:D13', 'Name', cell_format)
                sheet.merge_range('E13:F13', 'Gender', cell_format)

                # Body
                row = 13
                for rec in report:
                    row += 1
                    sheet.merge_range(f'A{row}:B{row}', rec['admission_no'], txt)
                    sheet.merge_range(f'C{row}:D{row}', rec['name'], txt)
                    sheet.merge_range(f'E{row}:F{row}', rec['gender'], txt)

            elif not department_name and not class_name:
                row = 10
                for dep in department_details:
                    for cls in class_details:
                        if dep['dep_id'] == cls['department_id']:
                            sheet.merge_range(f'A{row}:C{row}', f'Department Name : {dep["dept_name"]}', top_txt)
                            row += 1
                            sheet.merge_range(f'A{row}:C{row}', f'Class Name : {cls["class_name"]}', top_txt)
                            row += 2
                            sheet.merge_range(f'A{row}:B{row}', 'Admission Number', cell_format)
                            sheet.merge_range(f'C{row}:D{row}', 'Name', cell_format)
                            sheet.merge_range(f'E{row}:F{row}', 'Gender', cell_format)
                            for rec in report:
                                if cls['class_name'] == rec['class_name']:
                                    row += 1
                                    sheet.merge_range(f'A{row}:B{row}', rec['admission_no'], txt)
                                    sheet.merge_range(f'C{row}:D{row}', rec['name'], txt)
                                    sheet.merge_range(f'E{row}:F{row}', rec['gender'], txt)
                            row += 3

            elif not department_name and class_name:
                row = 10
                for dep in department_details:
                    for cls in class_details:
                        if dep['dep_id'] == cls['department_id'] and cls['class_name'] == class_name:
                            sheet.merge_range(f'A{row}:C{row}', f'Department Name : {dep["dept_name"]}', top_txt)
                            row += 1
                            sheet.merge_range(f'A{row}:C{row}', f'Class Name : {cls["class_name"]}', top_txt)
                            row += 2
                            sheet.merge_range(f'A{row}:B{row}', 'Admission Number', cell_format)
                            sheet.merge_range(f'C{row}:D{row}', 'Name', cell_format)
                            sheet.merge_range(f'E{row}:F{row}', 'Gender', cell_format)

                            for rec in report:
                                if dep['dep_id'] == rec['department_id'] and cls['class_name'] == class_name:
                                    row += 1
                                    sheet.merge_range(f'A{row}:B{row}', rec['admission_no'], txt)
                                    sheet.merge_range(f'C{row}:D{row}', rec['name'], txt)
                                    sheet.merge_range(f'E{row}:F{row}', rec['gender'], txt)
                            row += 3

            elif department_name and not class_name:
                row = 10
                for dep in department_details:
                    for cls in class_details:
                        if dep['dep_id'] == cls['department_id'] and dep['dept_name'] == department_name:
                            sheet.merge_range(f'A{row}:C{row}', f'Department Name : {dep["dept_name"]}', top_txt)
                            row += 1
                            sheet.merge_range(f'A{row}:C{row}', f'Class Name : {cls["class_name"]}', top_txt)
                            row += 2
                            sheet.merge_range(f'A{row}:B{row}', 'Admission Number', cell_format)
                            sheet.merge_range(f'C{row}:D{row}', 'Name', cell_format)
                            sheet.merge_range(f'E{row}:F{row}', 'Gender', cell_format)
                            for rec in report:
                                if cls['class_name'] == rec['class_name'] and dep['dept_name'] == department_name:
                                    row += 1
                                    sheet.merge_range(f'A{row}:B{row}', rec['admission_no'], txt)
                                    sheet.merge_range(f'C{row}:D{row}', rec['name'], txt)
                                    sheet.merge_range(f'E{row}:F{row}', rec['gender'], txt)
                            row += 3
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        else:
            raise ValidationError('There are no records...!')

