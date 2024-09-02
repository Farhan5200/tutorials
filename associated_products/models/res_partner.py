# -*- coding: utf-8 -*-

from odoo import fields,models

class ResPartner(models.Model):
    """to add a field in partner form view to add associated products """
    _inherit = "res.partner"

    associated_product_ids = fields.Many2many("product.product")
