# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import ValidationError


class SchoolStudentReport(models.AbstractModel):
    _name = "report.school_management.report_student"
    _description = "All student report"

    @api.model
    def _get_report_values(self, docids, data=None):

        class_name = data['class_name']
        department_name = data['department_name']
        student_name = data['student_name']
        selected_values={
            'selected_class': class_name,
            'selected_department': department_name,
            'selected_student': student_name
        }

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
                query += " where school_class.name = '%s' and school_department.name = '%s'" %(class_name, department_name)
        if class_name and not department_name:
            if student_name:
                query += " where student_registration.first_name = '%s'" % student_name
            else:
                query += " where school_class.name = '%s'" %class_name
        if not class_name and department_name:
            if student_name:
                query += " where student_registration.first_name = '%s'" % student_name
            else:
                query += " where school_department.name = '%s'" %department_name
        if not class_name and not department_name and student_name:
            query += " where student_registration.first_name = '%s'" % student_name




        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(department_query)
        department_details = self.env.cr.dictfetchall()
        self.env.cr.execute(class_query)
        class_details = self.env.cr.dictfetchall()

        if report:
            return {
                'docs': report,
                'selected_values': selected_values,
                'department_details': department_details,
                'class_details': class_details
            }
        else:
            raise ValidationError('There are no records...!')


