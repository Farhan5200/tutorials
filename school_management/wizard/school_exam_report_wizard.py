# -*- coding: utf-8 -*-

from odoo import api, fields,models

class SchoolExamReportWizard(models.TransientModel):
    _name = "school.exam.report.wizard"
    _description = "School Exam Report Wizard"


    def action_print_report(self):
        data={
        }

        return self.env.ref('school_management.action_report_school_exam').report_action(None, data=data)

class AllExamReport(models.AbstractModel):
    _name = "report.school_management.report_exam"
    _description = "All exam report"

    @api.model
    def _get_report_values(self, docids, data=None):

        query = """select * from school_exam"""

        print(query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        return {
            'docs': report
        }

