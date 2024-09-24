{
    'name': 'POS Rating nishal',
    'application': True,
    'version': '17.0.1.0.1',
    'summary': 'Rating filed in the POS',
    'description': """
This is a base module for setting a rating field in POS product view
    """,

    'depends': [
        'base',
        'product',
        'point_of_sale',
    ],

    'data': [
        'views/product.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'nishalkkk/static/src/xml/product_widget.xml',
            'nishalkkk/static/src/xml/pos_screen.xml',
            'nishalkkk/static/src/xml/pos_receipt.xml',

            'nishalkkk/static/src/js/pos_receipt.js',
        ],
    },

    'license': 'LGPL-3',

}
