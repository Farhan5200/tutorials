# -*- coding: utf-8 -*-

import logging
import pprint

import requests
from docutils.nodes import header
from werkzeug import urls
from ..const import DEFAULT_PAYMENT_METHODS_CODES
from odoo import api,fields,models

_logger = logging.getLogger(__name__)

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

    def _get_default_payment_method_codes(self):
        print('final')
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'multisafepay':
            return default_codes
        print('not final')
        default_multisafe_method = [
            'multisafe',
        ]
        return default_multisafe_method

    def _multisafe_make_request(self,api_key, data=None, method=None):
        print('third')
        self.ensure_one()
        if method=='POST':
            url = f'https://testapi.multisafepay.com/v1/json/orders?api_key={api_key}'
            headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json',
            }
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
            return response.json()
        else:
            # print(order,'or')
            url = f'https://testapi.multisafepay.com/v1/json/orders/{data}/?api_key={api_key}'
            headers = {
                'accept': 'application/json',
            }
            response = requests.request(method, url, headers=headers, timeout=60)
            return response.json()

