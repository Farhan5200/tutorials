# -*- coding: utf-8 -*-

{
    'name': 'QR Menu',
    'depends': ['base', 'base_setup', 'bus', 'web_tour', 'mail', 'web'],
    'data': [
        'views/ir_actions_client.xml',
        # 'security/ir.model.access.csv',
        # 'wizard/qr_generator_wizard.xml',
        # 'views/qr_generator_modal.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'qr_code_generator/static/src/xml/qr_generator_template.xml',
            'qr_code_generator/static/src/js/qr_code_component.js',
            'qr_code_generator/static/src/xml/qr_code_generator.xml',
            'qr_code_generator/static/src/js/qr_code_generator.js',
        ],
    },
}
