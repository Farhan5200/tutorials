# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    """to add associated products to the order line"""
    _inherit = "sale.order"

    is_associated_product = fields.Boolean(string="Associated products", default=False)

    @api.onchange('is_associated_product')
    def _onchange_associated_product(self):
        """this function is used to add product associated to partner in his sale order line"""
        associated_products = self.partner_id.associated_product_ids
        if self.is_associated_product:
            for rec in associated_products:
                self.order_line = [fields.Command.create({
                    'product_id': rec.id,
                    'product_uom_qty': 1,
                    'is_associated': True,
                })]
        else:
            order_line_products = self.order_line
            for rec in order_line_products:
                if rec.is_associated:
                    self.order_line = [fields.Command.unlink(rec.id)]


class SaleOrderLine(models.Model):
    """to add a boolean field in order line"""
    _inherit = "sale.order.line"

    is_associated = fields.Boolean(default=False)
