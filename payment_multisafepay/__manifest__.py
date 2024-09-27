# -*- coding: utf-8 -*-

{
    'name': 'Payment Provider: MultiSafePay',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': "A payment provider",
    'description': "Redirects to MultiSafePay payment site",
    'depends': ['payment', 'base'],
    'data': [
        'views/payment_multisafe_templates.xml',
        'data/payment_method.xml',
        'data/account_payment_method.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'installable': True,
}
