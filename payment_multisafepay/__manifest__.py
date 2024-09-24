# -*- coding: utf-8 -*-

{
    'name': 'Payment Provider: MultiSafePay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': "A payment provider",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment', 'base'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
}
