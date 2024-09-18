# -*- coding: utf-8 -*-

{
    'name': 'Pos Rating',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_rating/static/src/xml/product_card.xml',
        ],
    },
}