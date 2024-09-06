# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import ValidationError


class SchoolExamReport(models.AbstractModel):
    """For passing values to the exam report"""

    _name = "report.school_management.report_exam"
    _description = "All exam report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """For passing values to the exam report"""

        class_name = data['class_name']
        exam_name = data['exam_name']

        exam_query = """select school_exam.name as exam_name, school_exam.start_date as start_date, school_exam.end_date as 
        end_date, school_class.name as class_name from(school_exam inner join school_class on school_exam.class_id = 
        school_class.id)"""

        paper_query = """select school_subject.name as exam_paper, school_exam_paper.pass_mark, school_exam_paper.max_mark,
         school_exam.name as exam_name from (school_exam_paper inner join school_subject on school_subject.id = 
         school_exam_paper.subject_id) inner join school_exam on school_exam.id = school_exam_paper.exam_id"""

        if class_name and not exam_name:
            exam_query += " where school_class.name = '%s'" %class_name
        if exam_name and not class_name:
            exam_query += " where school_exam.name = '%s'" %exam_name
        if exam_name and class_name:
            exam_query += " where school_class.name = '%s' and school_exam.name = '%s'" %(class_name, exam_name)



        self.env.cr.execute(exam_query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(paper_query)
        paper = self.env.cr.dictfetchall()
        if report:
            return {
                'docs': report,
                'paper': paper
            }
        else:
            raise ValidationError('No records.....!')

