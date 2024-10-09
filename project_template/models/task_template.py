# -*- coding: utf-8 -*-

from odoo import fields,models

class TaskTemplate(models.Model):
    _name = 'task.template'

    name = fields.Char()


