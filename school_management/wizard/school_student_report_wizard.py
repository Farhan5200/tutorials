# -*- coding: utf-8 -*-

from odoo import api, fields,models
from odoo.tools import json


class SchoolStudentReportWizard(models.TransientModel):
    _name = "school.student.report.wizard"
    _description = "School Student Report Wizard"

    department_id = fields.Many2one('school.department', string="department")
    class_id = fields.Many2one('school.class', string="Class")
    # class_domain = fields.Char(compute="_onchange_department_id")


    # @api.onchange('department_id')
    # def _onchange_department_id(self):
    #     self.class_domain = "[()]"
    #     if self.department_id:
    #         self.class_domain = json.dumps([('department_id', '=', 'department_id')])
    #     print(self.class_domain)



    def action_print_report(self):
        data={
            'class_name': self.class_id.name,
            'department_name': self.department_id.name
        }

        return self.env.ref('school_management.action_report_school_student').report_action(None, data=data)

class AllStudentReport(models.AbstractModel):
    _name = "report.school_management.report_student"
    _description = "All student report"

    @api.model
    def _get_report_values(self, docids, data=None):

        class_name = data['class_name']
        department_name = data['department_name']

        query = """select student_registration.name as admission_no, student_registration.first_name as name, 
        school_class.name as class_name, school_department.name as department_name, student_registration.gender as 
        gender from((student_registration inner join school_class on school_class.id = 
        student_registration.current_class_id)inner join school_department on school_class.department_id = 
        school_department.id)"""

        if class_name and department_name:
            query += " where school_class.name = '%s' and school_department.name = '%s'" %(class_name, department_name)
        if class_name and not department_name:
            query += " where school_class.name = '%s'" %class_name
        if not class_name and department_name:
            query += " where school_department.name = '%s'" %department_name

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        return {
            'docs': report
        }

