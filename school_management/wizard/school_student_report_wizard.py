# -*- coding: utf-8 -*-

from odoo import api, fields,models


class SchoolStudentReportWizard(models.TransientModel):
    """For student report wizard"""

    _name = "school.student.report.wizard"
    _description = "School Student Report Wizard"

    department_id = fields.Many2one('school.department', string="Department")
    class_id = fields.Many2one('school.class', string="Class")
    class_domain_ids = fields.Many2many('school.class', compute="_compute_department_id_class_id")
    student_id = fields.Many2one('student.registration', string="Student")
    student_domain_ids = fields.Many2many('student.registration', compute='_compute_department_id_class_id')



    @api.depends('department_id', 'class_id')
    def _compute_department_id_class_id(self):
        """Dynamic domain for student_id and class_id"""
        for rec in self:
            if not rec.department_id:
                rec.class_domain_ids = rec.env['school.class'].search([])
                rec.student_domain_ids = rec.env['student.registration'].search([])
            else:
                rec.class_domain_ids = rec.env['school.class'].search([('department_id', '=', rec.department_id.id)])
                rec.student_domain_ids = rec.env['student.registration'].search([('current_class_id.department_id', '=', rec.department_id.id)])
            if self.class_id:
                rec.student_domain_ids = rec.env['student.registration'].search([('current_class_id', '=', rec.class_id.id)])

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.class_id = False
        self.student_id = False

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.student_id = False


    def action_print_report(self):
        """For printing student report"""

        data={
            'class_name': self.class_id.name,
            'department_name': self.department_id.name,
            'student_name': self.student_id.first_name
        }

        return self.env.ref('school_management.action_report_school_student').report_action(None, data=data)

