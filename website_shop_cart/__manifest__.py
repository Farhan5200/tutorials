# -*- coding: utf-8 -*-

{
    'name': 'Website Shop Cart',
    'version': '17.0.1.0.0',
    'summary': 'add to cart button and quantity button in shop homepage',
    'description': 'this will add a quantity button and add to cart button in shop main page user can directly add '
                   'product to cart from there',
    'depends': [
        'base',
        'website_sale',
    ],
    'data': [
        'views/website_shop_template.xml',
        'views/website_snippet_options.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_shop_cart/static/src/js/website_shop_cart.js',
        ],
    },
    'application': True,
    'installable': True,
}
