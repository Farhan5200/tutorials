# -*- coding: utf-8 -*-

{
    'name':'Sale Report Automation',
    'depends':['base','sale'],
    'data':[
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/mail_template.xml',
        'views/sale_report_automation_views.xml',
        'data/cron_data.xml',
        'report/sale_pdf_report_template.xml',
        'report/ir_actions_report.xml',
    ],
}