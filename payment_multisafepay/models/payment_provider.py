# -*- coding: utf-8 -*-


from odoo import fields,models

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', 'MultiSafePay')], ondelete={'multisafepay': 'set default'}
    )
    multisafepay_api_key = fields.Char(
        string="MultiSafePay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        groups="base.group_system"
    )

    def demoooo(self):
        for rec in self.env['payment.provider'].search([]):
            if rec.code == 'multisafepay':
                print(rec.get_base_url())
                print(rec.multisafepay_api_key)
