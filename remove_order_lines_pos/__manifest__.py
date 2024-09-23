# -*- coding: utf-8 -*-

{
    'name': 'Remove order lines POS',
    'version': '17.0.1.0.0',
    'summary': 'To clear order lines with button',
    'description': 'adds two button one to clear selected line and another one to clear complete order line',
    'depends': [
        'base',
        'point_of_sale',
        'web',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'remove_order_lines_pos/static/src/xml/remove_selected_order_line.xml',
            'remove_order_lines_pos/static/src/js/remove_selected_order_line.js',
            'remove_order_lines_pos/static/src/xml/remove_all_order_line.xml',
            'remove_order_lines_pos/static/src/js/remove_all_order_line_pos.js',
        ],
    },
    'installable': True,
}
