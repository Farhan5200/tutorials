# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMove(models.Model):
    """to add a field to invoice for selecting multiple sale orders """
    _inherit = "account.move"

    related_sale_order_ids = fields.Many2many('sale.order', domain="[('partner_id', '=', partner_id), ('invoice_status', '=', 'to invoice')]")

    @api.onchange('related_sale_order_ids')
    def _onchange_related_sale_order_ids(self):
        """to add sale order lines to the invoice"""
        self.invoice_line_ids = [fields.Command.clear()]
        for rec in self.related_sale_order_ids.order_line:
            if not rec.invoice_lines:
                self.invoice_line_ids = [fields.Command.create({
                    'product_id': rec.product_id,
                    'related_sale_order_id': rec.order_id,
                    'order_line_id': rec.id
                })]

    def action_post(self):
        """to link sale order with this invoice. there is a field invoice_lines in sale_order_line which link
        sale order lines with invoice lines so this function is to link invoice lines to the corresponding
        sale order lines"""
        for rec in self.invoice_line_ids:
            for records in self.invoice_line_ids.related_sale_order_id.order_line:
                if rec.order_line_id.id == records.id:
                    records.invoice_lines = [fields.Command.link(rec.id)]
        print("hiiiiiiiiiii")
        print("biiiiiiiiiii")
        return super().action_post()


class AccountMoveLine(models.Model):
    """add two fields to the invoice line"""
    _inherit = 'account.move.line'

    related_sale_order_id = fields.Many2one('sale.order')
    order_line_id = fields.Many2one('sale.order.line')

