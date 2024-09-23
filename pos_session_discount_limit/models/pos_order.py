# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosOrder(models.Model):
    """to add a field and to send total discount to pos"""
    _inherit = 'pos.order'

    total_discount_amount = fields.Float(string="Total Discount Amount", compute="_compute_total_discount_amount")

    @api.depends('lines')
    def _compute_total_discount_amount(self):
        """computes total discount amount of the order"""
        for rec in self:
            total_discount_amount = 0
            for records in rec.lines:
                if records.price_unit < 0:
                    total_discount_amount += (records.discount_amount - records.price_subtotal_incl)
                else:
                    total_discount_amount += records.discount_amount
                rec.total_discount_amount = total_discount_amount

    @api.model
    def send_total_discount_pos(self, pos_session_id):
        """sends the total discount amount of all orders in currently opened session to pos"""
        records = self.search([('session_id', '=', pos_session_id)])
        total_discount = 0
        for rec in records:
            total_discount += rec.total_discount_amount
        return total_discount

    @api.model
    def send_product_tax(self,product_id):
        """returns tax amount of the discount product"""
        return self.env['product.product'].browse(product_id).taxes_id.amount


class PosOrderLine(models.Model):
    """to add a field to show discount amount of order line"""
    _inherit = 'pos.order.line'

    discount_amount = fields.Float(string="Discount Amount", compute="_compute_discount_amount")

    @api.depends('qty', 'price_unit', 'discount')
    def _compute_discount_amount(self):
        """to compute discount amount of each order line"""
        for rec in self:
            if rec.tax_ids_after_fiscal_position.amount:
                rec.discount_amount = (rec.qty * rec.price_unit * (
                            (rec.tax_ids_after_fiscal_position.amount + 100) / 100)) * (
                                              rec.discount / 100)
            else:
                rec.discount_amount = rec.qty * rec.price_unit * (rec.discount / 100)

