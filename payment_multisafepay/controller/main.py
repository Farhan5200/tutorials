# -*- coding: utf-8 -*-

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MultiSafeController(http.Controller):
    _return_url = '/payment/multisafe/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def multisafe_return_from_checkout(self, **data):
        """ Process the notification data sent by MultiSafePay after redirection from checkout.
        :param dict data: The notification data (only `id`) and the transaction reference (`ref`)
                          embedded in the return URL
        """
        _logger.info("handling redirection from Mollie with data:\n%s", pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')