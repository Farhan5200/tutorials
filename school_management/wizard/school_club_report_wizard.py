# -*- coding: utf-8 -*-

from odoo import api, fields,models

class SchoolClubReportWizard(models.TransientModel):
    _name = "school.club.report.wizard"
    _description = "School Club Report Wizard"

    club_id = fields.Many2one('school.club', string="Club")

    def action_print_report(self):
        data={
            'club_name': self.club_id.name
        }

        return self.env.ref('school_management.action_report_school_club').report_action(None, data=data)

class AllClubReport(models.AbstractModel):
    _name = "report.school_management.report_club"
    _description = "All club report"

    @api.model
    def _get_report_values(self, docids, data=None):
        club_name = data['club_name']

        query = """select school_club.name as club_name ,student_registration.first_name as student_name from
         ((school_club inner join school_club_student_registration_rel on school_club.id = 
         school_club_student_registration_rel.school_club_id) inner join student_registration on
          student_registration.id = school_club_student_registration_rel.student_registration_id)"""

        print(query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        return {
            'docs': report
        }

