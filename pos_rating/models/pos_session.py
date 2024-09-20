# -*- coding: utf-8 -*-

from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """to load rating field in pos"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['rating'])
        return result
