# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    """to check weather the discount given in sale order line is greater than the discount limit given inside
     settings and to add new value to status bar and also to add new button"""
    _inherit = 'sale.order'

    SALE_ORDER_STATE = [
        ('draft', "Quotation"),
        ('to_approve', "To Approve"),
        ('sent', "Quotation Sent"),
        ('sale', "Sales Order"),
        ('cancel', "Cancelled"),
    ]

    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    total_amount_calculated = fields.Float(store=True, compute="_compute_total_amount_calculated")

    @api.depends('order_line')
    def _compute_total_amount_calculated(self):
        total_amount = 0
        for rec in self.order_line:
            tax = rec.tax_id.amount
            qty = rec.product_uom_qty
            unit_price = rec.price_unit
            if unit_price > 0:
                if tax > 0:
                    total_amount += (qty * unit_price) * ((tax + 100) / 100)
                else:
                    total_amount += (qty * unit_price)
        for rec in self:
            rec.total_amount_calculated = total_amount

    def check_user(self):
        """if the user is manager it performs normal confirm button action else it will change the state to approve """
        if self.user_has_groups('sales_team.group_sale_manager'):
            return super().action_confirm()
        else:
            self.state = 'to_approve'

    def action_confirm(self):
        """to check weather the discount given in sale order line is greater than the discount limit given inside
     settings if it is greater then only manager can approve"""
        is_set_limit = self.env['ir.config_parameter'].sudo().get_param('base.set_limit')
        if is_set_limit:
            discount_limit = float(self.env['ir.config_parameter'].sudo().get_param('base.discount_limit'))
            fixed_price = float(self.env['ir.config_parameter'].sudo().get_param('base.fixed_price'))
            select_type = self.env['ir.config_parameter'].sudo().get_param('base.select_type')
            if select_type == 'percentage':
                if self.total_amount_calculated - (self.total_amount_calculated * discount_limit) > self.amount_total:
                    self.check_user()
                else:
                    return super().action_confirm()
            elif select_type == 'fixed_amount':
                if self.total_amount_calculated - fixed_price > self.amount_total:
                    self.check_user()
                else:
                    return super().action_confirm()
        else:
            return super().action_confirm()

    def action_approve(self):
        return super().action_confirm()

    def _can_be_confirmed(self):
        """returns true if state in draft, sent, to_approve"""
        self.ensure_one()
        return self.state in {'draft', 'sent', 'to_approve'}

