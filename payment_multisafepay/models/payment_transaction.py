# -*- coding: utf-8 -*-

import logging
import pprint

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
from ..controller.main import MultiSafeController


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"
    
    def _get_specific_rendering_values(self, processing_values):
        """redirects to the payment page"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res
        api_key = self.provider_id.multisafepay_api_key
        payload = self._multisafe_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._multisafe_make_request(api_key=api_key, data=payload, method='POST')
        self.provider_reference = payment_data['data']['order_id']
        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _multisafe_prepare_payment_request_payload(self):
        """prepares the data to be send to the url"""
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultiSafeController._return_url)

        return {
            "type": "redirect",
            "order_id": self.id,
            "gateway": "",
            "currency": self.currency_id.name,
            "amount": self.amount*100,
            "description": "Test order description",
            "payment_options": {
                "notification_url": "https://www.example.com/client/notification?type=notification",
                "notification_method": "POST",
                "redirect_url": f'{redirect_url}?ref={self.reference}',
                "cancel_url": "https://www.example.com/client/notification?type=cancel",
                "close_window": True
            },
            "customer": {
                "locale": self.partner_lang,
                "ip_address": "123.123.123.123",
                "first_name": self.partner_name,
                "last_name": self.partner_name,
                "company_name": "Test Company Name",
                "address1": self.partner_address,
                "house_number": self.partner_address,
                "zip_code": self.partner_zip,
                "city": self.partner_city,
                "country": self.partner_country_id.name,
                "phone": self.partner_phone,
                "email": self.partner_email,
            }
        }
    
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on MultiSafePay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('ref')), ('provider_code', '=', 'multisafepay')]
        )
        if not tx:
            raise ValidationError("MultiSafePay: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        tx._process_notification_data(notification_data)
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on MultiSafePay data.
        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return
        transaction_id = notification_data['transactionid']
        api_key = self.provider_id.multisafepay_api_key
        payment_data = self.provider_id._multisafe_make_request(api_key=api_key, data=transaction_id, method='GET')
        payment_status = payment_data['data']['status']
        if payment_status in ['initialized', 'uncleared']:
            self._set_pending()
        elif payment_status in ['completed','shipped']:
            self._set_done()
        elif payment_status in ['void', 'cancel', 'declined']:
            self._set_canceled("MultiSafePay: " + _("Canceled payment with status: %s", payment_status))
        else:
            self._set_error('Error')
        
