# -*- coding: utf-8 -*-

{
    'name': 'School Management',
    'version': '17.0.6.0.0',
    'summary': 'manage students, employees, staffs,  registration and departments in school',
    'description': 'for managing student registration and departments in school',
    'depends': [
        'base',
        'web',
        'mail',
        'sale',
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
        'views/student_registration_website_template.xml',
        'views/events_website_template.xml',
        # data
        'data/mail_template_data.xml',
        'data/cron_data.xml',
        'data/ir_actions_server_data.xml',
        'data/automation_data.xml',
        'data/ir_sequence_data.xml',
        'data/school_department_data.xml',
        'data/school_subject_data.xml',
        'data/school_class_data.xml',
        # report
        'report/school_event_templates.xml',
        'report/school_club_templates.xml',
        'report/school_exam_templates.xml',
        'report/school_leave_templates.xml',
        'report/school_student_templates.xml',
        'report/ir_actions_report.xml',
        # wizard
        'wizard/school_event_report_wizard_views.xml',
        'wizard/school_club_report_wizard_views.xml',
        'wizard/school_exam_report_wizard_views.xml',
        'wizard/school_leave_report_wizard_views.xml',
        'wizard/school_student_report_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': ['school_management/static/src/js/action_manager.js']
    },
    'application': True,
    'installable': True,
}
