{
    'name': 'Hospital',
    'application': True,
    'depends': [
        'contacts',
        'hr',
        'base'
    ],
        'data': [
            'security/ir.model.access.csv',
            'views/hospital_patient_view.xml',
            'views/hospital_employee_view.xml',
            'views/hospital_department_view.xml',
            'views/hospital_consultation_view.xml',
            'views/hospital_op_ticket_view.xml'
        ]

}
