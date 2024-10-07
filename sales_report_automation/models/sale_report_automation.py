# -*- coding: utf-8 -*-
import base64

from dateutil.utils import today

from odoo import _,api,fields,models
from datetime import datetime
from odoo.tools import date_utils



class SaleReportAutomation(models.Model):
    _name = "sale.report.automation"
    _description = "Sale Report Automation"

    name = fields.Char("Sequence no", required=True, default=lambda self: _('New'), copy=False, readonly=True,
                       tracking=True)
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
            for rec in self.partner_ids:
                data = {
                    'selected_interval': self.report_type,
                    'selected_from_date': self.from_date,
                    'selected_to_date': self.to_date,
                    'selected_sales_team': self.sales_team_id.id,
                    'selected_partner': rec.id,
                }
                start_date = self.from_date
                end_date = self.to_date
                today_date = fields.Date.today()
                this_month_start = date_utils.start_of(today_date, "month")
                this_month_end = date_utils.end_of(today_date, "month")
                this_week_start = date_utils.start_of(today_date, "week")
                this_week_end = date_utils.end_of(today_date, "week")
                if self.report_type == 'monthly':
                    print('monthhhhhlyyyy')
                    sale_report = self.env.ref('sales_report_automation.action_report_sale_pdf')
                    data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(sale_report, [self.id], data=data)[0])
                    print(data_record)
                    ir_values = {
                        'name': f'Sale report of {rec.name} from {this_month_start} to {this_month_end}',
                        'type': 'binary',
                        'datas': data_record,
                        'store_fname': data_record,
                        'mimetype': 'application/pdf',
                        'res_model': 'sale.report.automation',
                    }
                    sale_report_attachment_id = self.env['ir.attachment'].sudo().create(ir_values)
                    print(sale_report_attachment_id)
                    if sale_report_attachment_id:
                        email_template = self.env.ref(
                            'sales_report_automation.sale_report_mail_template')
                        if rec.email:
                            email = rec.email
                        else:
                            email = 'admin@example.com'
                        print(email_template)
                        if email_template and email:
                            email_values = {
                                'email_to': email,
                                'email_cc': False,
                                'scheduled_date': False,
                                'recipient_ids': [],
                                'partner_ids': [],
                                'auto_delete': True,
                            }
                            email_template.attachment_ids = [
                                (4, sale_report_attachment_id.id)]
                            email_template.with_context(context = {'partner_name': rec.name,
                                                                   'report_type': 'Monthly',
                                                                   'from_date': this_month_start,
                                                                   'to_date': this_month_end,
                                                                   }).send_mail(
                                self.id, email_values=email_values, force_send=True)
                            email_template.attachment_ids = [(5, 0, 0)]





                    if (start_date <= today_date) and (end_date >= today_date):
                        if today_date == this_month_end:
                            print('send monthly report')
                else:
                    print('weeeklllyyyyyy')
                    sale_report = self.env.ref('sales_report_automation.action_report_sale_pdf')
                    data_record = base64.b64encode(
                        self.env['ir.actions.report'].sudo()._render_qweb_pdf(sale_report, [self.id], data=data)[0])
                    print(data_record)
                    ir_values = {
                        'name': f'Sale report of {rec.name} from {this_week_start} to {this_week_end}',
                        'type': 'binary',
                        'datas': data_record,
                        'store_fname': data_record,
                        'mimetype': 'application/pdf',
                        'res_model': 'sale.report.automation',
                    }
                    sale_report_attachment_id = self.env['ir.attachment'].sudo().create(ir_values)
                    print(sale_report_attachment_id)
                    if sale_report_attachment_id:
                        email_template = self.env.ref(
                            'sales_report_automation.sale_report_mail_template')
                        if rec.email:
                            email = rec.email
                        else:
                            email = 'admin@example.com'
                        print(email_template)
                        if email_template and email:
                            email_values = {
                                'email_to': email,
                                'email_cc': False,
                                'scheduled_date': False,
                                'recipient_ids': [],
                                'partner_ids': [],
                                'auto_delete': True,
                            }
                            email_template.attachment_ids = [
                                (4, sale_report_attachment_id.id)]
                            email_template.with_context(context={'partner_name': rec.name,
                                                                 'report_type': 'Weekly',
                                                                 'from_date': this_week_start,
                                                                 'to_date': this_week_end,
                                                                 }).send_mail(
                                self.id, email_values=email_values, force_send=True)
                            email_template.attachment_ids = [(5, 0, 0)]


                    if (start_date <= today_date) and (end_date >= today_date):
                        if today_date == this_week_end:
                            print('send weekly report')

    def scheduled_action_send_mail(self):
        events = self.search([])
        for rec in events:
            rec.action_send_sales_report()

    def action_print_sale_pdf_report(self):
        data = {
            'selected_interval': self.report_type,
            'selected_from_date':self.from_date,
            'selected_to_date':self.to_date,
            'selected_sales_team':self.sales_team_id.id,
            'selected_partner':self.partner_ids.ids,
        }

        return self.env.ref('sales_report_automation.action_report_sale_pdf').report_action(None, data=data)

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = (self.env['ir.sequence'].
                                  next_by_code('sale.report.automation'))
        return super().create(vals_list)
