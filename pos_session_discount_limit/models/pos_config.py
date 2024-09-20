# -*- coding: utf-8 -*-

from odoo import fields,models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    set_session_wise_limit = fields.Boolean(string="Set Session Wise Discount Limit")
    session_wise_discount_limit = fields.Float(string="Limit")
