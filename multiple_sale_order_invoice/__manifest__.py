# -*- coding: utf-8 -*-

{
    'name': 'Multiple Sale Order Invoice',
    'version': '17.0.1.0.0',
    'summary':'to create one invoice for multiple sale orders',
    'description':'we can select multiple sale orders while creating invoice and those sale order lines will be '
                  'added to the invoice lines',
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
}