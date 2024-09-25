# -*- coding: utf-8 -*-


from odoo import models

class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"
    
    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        print(processing_values)
        print('hi')
        if self.provider_code != 'multisafepay':
            return res
