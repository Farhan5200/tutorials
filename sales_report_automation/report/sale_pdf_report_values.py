# -*- coding: utf-8 -*-


from odoo import api, fields, models
from odoo.tools import date_utils


class SalePDFReportValues(models.AbstractModel):
    _name = "report.sales_report_automation.sale_pdf_report_template"
    _description = "Sale Pdf report"

    @api.model
    def _get_report_values(self, docids, data=None):
        print('nooo')
        details = self.env['sale.order'].search([])
        today = fields.Date.today()

        selected_interval = data['selected_interval']
        selected_from_date = data['selected_from_date']
        selected_to_date = data['selected_to_date']
        selected_sales_team = data['selected_sales_team']
        selected_partner = data['selected_partner']

        if selected_interval == 'monthly':
            selected_from_date = date_utils.start_of(today, "month")
            selected_to_date = date_utils.end_of(today, "month")
        if selected_interval == 'weekly':
            selected_from_date = date_utils.start_of(today, "week")
            selected_to_date = date_utils.end_of(today, "week")

        print(selected_interval, selected_from_date, selected_to_date, selected_sales_team, selected_partner)
        if selected_sales_team and not selected_partner:
            details = self.env['sale.order'].search(
                [('team_id', '=', selected_sales_team), ('date_order', '>=', selected_from_date),
                 ('date_order', '<=', selected_to_date)])
        elif selected_partner and not selected_sales_team:
            details = self.env['sale.order'].search(
                [('partner_id', '=', selected_partner), ('date_order', '>=', selected_from_date),
                 ('date_order', '<=', selected_to_date)])
        elif selected_sales_team and selected_partner:
            print('hii')
            details = self.env['sale.order'].search(
                [('team_id', '=', selected_sales_team), ('partner_id', '=', selected_partner),
                 ('date_order', '>=', selected_from_date), ('date_order', '<=', selected_to_date)])
        else:
            details = self.env['sale.order'].search(
                [('date_order', '>=', selected_from_date), ('date_order', '<=', selected_to_date)])

        return {
            'docs': details,
            'selected_from_date': selected_from_date,
            'selected_to_date':selected_to_date
        }
