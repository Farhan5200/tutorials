# -*- coding: utf-8 -*-

{
    'name': 'POS Rating',
    'version': '17.0.1.0.0',
    'summary': 'to add ratings of the product in pos screen and receipt',
    'description': 'adds a rating field in product form page and shows the rating of the product in pos screen and receipt',
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
            'pos_rating/static/src/js/custom_receipt.js',
            'pos_rating/static/src/xml/custom_rating.xml',
        ],
    },
    'installable': True,
}
