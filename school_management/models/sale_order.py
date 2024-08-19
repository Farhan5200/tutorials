# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    """to add admitted stage to the sale order"""
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])
