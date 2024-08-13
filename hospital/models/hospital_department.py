from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    name = fields.Char(string="Department Name")
    block = fields.Char("Block")
    manager_id = fields.Many2one("hr.employee", string="Head")
    doctor_id = fields.Many2many("hr.employee", string="Doctor")
