# -*- coding: utf-8 -*-

{
    'name': 'POS Session Discount Limit',
    'version': '17.0.1.0.0',
    'summary': 'To manage session wise discount limt',
    'description': 'Adds a field in settings to set discount limit and if session wise discount exceeds the limit it shows a popup',
    'depends': [
        'base',
        'point_of_sale',
        'web',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_session_discount_limit/static/src/js/order.js',
        ],
    },
    'installable': True,
}
