# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolEventReportWizard(models.TransientModel):
    _name = "school.event.report.wizard"
    _description = "School Event Report Wizard"

    def demo(self):
        data = {

            'doc_ids': self.env['school.event'].search([])
        }
        # docids = self.env['school.event'].search([])
        return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)
        # return {
        #     'type': 'ir.actions.report',
        #     'report_name': 'school_management.report_event',
        # }