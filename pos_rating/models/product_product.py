# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductProduct(models.Model):
    """to add a new rating field in product form page"""
    _inherit = "product.product"

    rating = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6')
        ], string='Ratings'
    )
