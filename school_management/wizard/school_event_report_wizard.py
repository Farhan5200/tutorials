# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolEventReportWizard(models.TransientModel):
    _name = "school.event.report.wizard"
    _description = "School Event Report Wizard"

    start_date = fields.Date(string="From", required=True)
    end_date = fields.Date(string="To",  required=True)

    def demo(self):
        print(self.env['school.event'].search_read([]))
        data = {
            'form': self.read()[0],
            'events': self.env['school.event'].search_read([])

        }
        # docids = self.env['school.event'].search([])
        return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)
        # return {
        #     'type': 'ir.actions.report',
        #     'report_name': 'school_management.report_event',
        # }