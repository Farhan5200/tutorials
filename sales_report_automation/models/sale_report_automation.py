# -*- coding: utf-8 -*-
from dateutil.utils import today

from odoo import api,fields,models
from datetime import datetime
from odoo.tools import date_utils



class SaleReportAutomation(models.Model):
    _name = "sale.report.automation"
    _description = "Sale Report Automation"

    report_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
    ], string="Report type", default="monthly", required=True)
    state = fields.Selection([
        ('running','Running'),
        ('cancelled','Cancelled')
    ])

    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")
    sales_team_id = fields.Many2one('crm.team', string="Sales Team")
    partner_ids = fields.Many2many('res.partner', string="Customer")

    def action_send_sales_report(self):
        if self.state == 'running':
            start_date = self.from_date
            end_date = self.to_date
            today_date = fields.Date.today()
            this_month_end = date_utils.end_of(today_date, "month")
            this_week_end = date_utils.end_of(today_date, "week")
            if self.report_type == 'monthly':
                if (start_date <= today_date) and (end_date >= today_date):
                    if today_date == this_month_end:
                        print('send monthly report')
            else:
                if (start_date <= today_date) and (end_date >= today_date):
                    if today_date == this_week_end:
                        print('send weekly report')

            # fmt = '%Y-%m-%d'
            # d1 = datetime.strptime(start_date, fmt)
            # d2 = datetime.strptime(end_date, fmt)
            # date_difference = int(((d2 - d1).days)/30)+1
        # self.env['ir.cron'].create({
        #     'name':'Sale Report Email'
        #     ''
        # })

        # data = {
        #     'selected_interval': self.interval,
        #     'selected_from_date':self.from_date,
        #     'selected_to_date':self.to_date,
        #     'selected_sales_team':self.sales_team_id.id,
        #     'selected_partner':self.partner_ids.ids,
        # }
        #
        # return self.env.ref('sales_report.action_report_sale_pdf').report_action(None, data=data)

    # @api.model_create_multi
    # def create(self, vals):
    #     events = super(SalePDFReport, self).create(vals)
    #     # self.create_scheduled_action()
    #     return events
