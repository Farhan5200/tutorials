# -*- coding: utf-8 -*-

from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    """to add field's in settings"""
    _inherit = "res.config.settings"

    pos_set_session_wise_limit = fields.Boolean(string="Set Session Wise Discount Limit", related="pos_config_id.set_session_wise_limit", readonly=False)
    pos_session_wise_discount_limit = fields.Float(string="Limit", related="pos_config_id.session_wise_discount_limit", readonly=False)
