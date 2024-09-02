# -*- coding: utf-8 -*-

{
    'name': 'Associated Products',
    'version': '17.0.1.0.0',
    'summary': 'to manage product associated with partner',
    'description': 'this will add a field in partner creation form to add products associated'
                   ' to partner and there will be a boolean field in sale order if it is enabled the products '
                   'associated to the partner will be added to sale order line',
    'depends': [
        'base',
        'product',
        'sale',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
