# -*- coding: utf-8 -*-

{
    'name': 'Discount Approval',
    'version': '17.0.1.0.0',
    'summary': 'to manage discount',
    'description': 'if the discount in order line is greater than the discount limit given in settings then only'
                   ' manager can confirm the quotation',
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'views/res_config_settings_view_form.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
