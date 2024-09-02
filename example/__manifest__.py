# -*- coding: utf-8 -*-

{
    'name': "example module",
    'version': '17.0.1.0.0',
    'application': True,
    'sequence': -100,

    'depends': [
        'base',
        'product',
    ],

    'data' : [
        'views/example_views.xml',
        'views/example_example_views.xml',
        'security/ir.model.access.csv',
    ]
}