# -*- coding: utf-8 -*-

from odoo import fields,models


class SchoolExamPaper(models.Model):
    """used to store paper's used in exam"""
    _name = 'school.exam.paper'
    _description = "School Exam Paper"

    subject_id = fields.Many2one("school.subject")
    pass_mark = fields.Integer()
    max_mark = fields.Integer()
    exam_id = fields.Many2one("school.exam")
