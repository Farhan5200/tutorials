# -*- coding: utf-8 -*-

from odoo import api, fields,models
from odoo.exceptions import ValidationError


class SchoolExamReportWizard(models.TransientModel):
    _name = "school.exam.report.wizard"
    _description = "School Exam Report Wizard"

    exam_id = fields.Many2one('school.exam', string="Exam")
    class_id = fields.Many2one('school.class', string="Class")
    exam_domain_ids = fields.Many2many('school.exam', compute="_compute_exam_domain_ids")


    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.exam_id = False

    @api.depends('class_id')
    def _compute_exam_domain_ids(self):
        for rec in self:
            if not rec.class_id:
                rec.exam_domain_ids = rec.env['school.exam'].search([])
            else:
                rec.exam_domain_ids = rec.env['school.exam'].search([('class_id', '=', rec.class_id.id)])




    def action_print_report(self):
        data={
            'class_name': self.class_id.name,
            'exam_name': self.exam_id.name
        }

        return self.env.ref('school_management.action_report_school_exam').report_action(None, data=data)

