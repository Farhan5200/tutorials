# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolClubReportWizard(models.TransientModel):
    _name = "school.club.report.wizard"
    _description = "School Club Report Wizard"

    club_id = fields.Many2many('school.club', string="Club")

    def action_print_report(self):
        data = {
            'selected_club': self.club_id.ids
        }


        return self.env.ref('school_management.action_report_school_club').report_action(None, data=data)


class AllClubReport(models.AbstractModel):
    _name = "report.school_management.report_club"
    _description = "All club report"

    @api.model
    def _get_report_values(self, docids, data=None):

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
            return {
                'docs': report,
                'all_club': club_name
            }
        else:
            raise ValidationError('No records.....!')
