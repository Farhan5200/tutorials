# -*- coding: utf-8 -*-

from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    """to add field's in settings"""
    _inherit = "res.config.settings"

    set_limit = fields.Boolean(string="Set Limit", config_parameter="base.set_limit")
    discount_limit = fields.Float(string="Percentage", config_parameter="base.discount_limit", default=0.1)
    fixed_price = fields.Float(string="Fixed amount", config_parameter="base.fixed_price", default=100)
    select_type = fields.Selection([
        ('percentage','Percentage'),
        ('fixed_amount','Fixed amount'),
    ], config_parameter="base.select_type", default="percentage")
    