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


