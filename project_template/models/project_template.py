# -*- coding: utf-8 -*-

from odoo import fields,models


class ProjectTemplate(models.Model):
    _name = 'project.template'
    _inherits = 'project.project'

    def demo(self):
        print('hi')
