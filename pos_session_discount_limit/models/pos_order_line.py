# -*- coding: utf-8 -*-

from odoo import api,fields,models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_discount_amount = fields.Float(string="Total Discount Amount", compute="_compute_total_discount_amount")

    @api.depends()
    def _compute_total_discount_amount(self):
        for rec in self:
            total_discount_amount = 0
            for records in rec.lines:
                total_discount_amount += records.discount_amount
                rec.total_discount_amount = total_discount_amount

    @api.model
    def send_total_discount_pos(self):
        print('kkbiii')


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'


    discount_amount = fields.Float(string="Discount Amount", compute="_compute_discount_amount")

    @api.depends('qty','price_unit','discount')
    def _compute_discount_amount(self):
        for rec in self:
            rec.discount_amount = rec.qty * rec.price_unit * (rec.discount/100)
