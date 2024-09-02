# -*- coding: utf-8 -*-

{
    'name': 'School Management',
    'version': '17.0.6.0.0',
    'summary': 'manage students, employees, staffs,  registration and departments in school',
    'description': 'for managing student registration and departments in school',
    'depends': [
        'base',
        'mail',
        'sale'
    ],
    'data': [
        'security/school_management_security_groups.xml',
        'security/school_management_security.xml',
        'security/ir.model.access.csv',
        'views/student_registration_views.xml',
        'views/school_club_views.xml',
        'views/school_event_views.xml',
        'views/res_partner_views.xml',
        'views/school_leaves_views.xml',
        'views/school_exam_views.xml',
        'views/school_department_views.xml',
        'views/school_class_views.xml',
        'views/school_subject_views.xml',
        'views/school_academic_year_views.xml',
        'views/sale_order_views.xml',
        'data/mail_template_data.xml',
        'data/cron_data.xml',
        'data/ir_actions_server_data.xml',
        'data/automation_data.xml',
        'data/ir_sequence_data.xml',
        'data/school_department_data.xml',
        'data/school_subject_data.xml',
        'data/school_class_data.xml',
    ],
    'application': True,
    'installable': True,
}
