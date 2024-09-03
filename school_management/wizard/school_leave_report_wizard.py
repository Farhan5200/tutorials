# -*- coding: utf-8 -*-

from odoo import api, fields,models

class SchoolLeaveReportWizard(models.TransientModel):
    _name = "school.leave.report.wizard"
    _description = "School Leave Report Wizard"


    def action_print_report(self):
        data={
        }

        return self.env.ref('school_management.action_report_school_leave').report_action(None, data=data)

class AllLeaveReport(models.AbstractModel):
    _name = "report.school_management.report_leave"
    _description = "All leave report"

    @api.model
    def _get_report_values(self, docids, data=None):

        query = """select * from school_leaves"""

        print(query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        return {
            'docs': report
        }

