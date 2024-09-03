# -*- coding: utf-8 -*-

from odoo import api, fields,models

class SchoolStudentReportWizard(models.TransientModel):
    _name = "school.student.report.wizard"
    _description = "School Student Report Wizard"


    def action_print_report(self):
        data={
        }

        return self.env.ref('school_management.action_report_school_student').report_action(None, data=data)

class AllStudentReport(models.AbstractModel):
    _name = "report.school_management.report_student"
    _description = "All student report"

    @api.model
    def _get_report_values(self, docids, data=None):

        query = """select * from student_registration"""

        print(query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        return {
            'docs': report
        }

