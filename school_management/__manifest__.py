# -*- coding: utf-8 -*-

{
    'name': 'School Management',
    'application': True,
    'installable': True,
    'version': '17.0.3.0.0',
    'summary': 'school management',
    'description': 'for managing student registration and departments in school',
    'data': [
        'security/ir.model.access.csv',
        'views/student_registration_views.xml',
        'views/school_club_views.xml',
        'views/school_event_views.xml',
        'views/school_department_views.xml',
        'views/school_class_views.xml',
        'views/school_subject_views.xml',
        'views/school_academic_year_views.xml',
        'views/sale_order_views.xml',
        'data/ir_sequence_data.xml',
        'data/school_department_data.xml',
        'data/school_subject_data.xml',
        'data/school_class_data.xml',
    ],
    'depends': [
        'base',
        'mail',
        'sale'
    ]
}
