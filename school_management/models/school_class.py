# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SchoolClass(models.Model):
    """used to create multiple classes in school"""
    _name = "school.class"
    _description = "School Class"
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    department_id = fields.Many2one("school.department", string="Department", tracking=True)
    head_of_department_id = fields.Many2one('res.partner', string="Head", tracking=True)
    school_id = fields.Many2one("res.company", string="School", tracking=True, default=lambda self: self.env.company)

    @api.onchange('department_id')
    def onchange_department_id(self):
        self.head_of_department_id = self.department_id.head_of_department_id
