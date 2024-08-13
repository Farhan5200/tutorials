from odoo import models, fields


class HospitalEmployee(models.Model):
    _inherit = 'hr.employee'

    age = fields.Integer("Employee Age")
    date_of_birth = fields.Date("Date Of Birth")
    employee_fees = fields.Integer("Fees")
    room_no = fields.Char("Room No : ")
    qualification = fields.Char("Qualification")
