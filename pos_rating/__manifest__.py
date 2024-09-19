# -*- coding: utf-8 -*-

{
    'name': 'Pos Rating',
    'depends': [
        'base',
        'product',
        'point_of_sale',
    ],
    'data': [
        'views/product_product_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_rating/static/src/xml/product_card.xml',
            'pos_rating/static/src/xml/product_widget.xml',
        ],
        'web.assets_backend': [
            'pos_rating/static/src/js/custom_receipt.js',
        ],
    },
}
