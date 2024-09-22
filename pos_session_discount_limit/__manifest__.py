# -*- coding: utf-8 -*-

{
    'name': 'POS Session Discount Limit',
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
}
