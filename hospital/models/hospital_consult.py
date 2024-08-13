from odoo import models, fields, api


class HospitalConsultation(models.Model):
    _name = "hospital.consultation"
    _description = "Hospital Consult"

    doctor_id = fields.Many2one("hr.employee", string="Doctor")
    patient_id = fields.Many2one("res.partner", string="Patient")
    department_id = fields.Many2one("hr.department", string="Department")
    date = fields.Date("Date")
    patient_prescription = fields.Text()
    patient_history = fields.Text()
    op_id = fields.Many2one("op.ticket", string="OP Number :")

    @api.onchange('op_id')
    def onchange_op_id(self):
        self.patient_id = self.op_id.patient_id
        self.doctor_id = self.op_id.doctor_id
        self.date = self.op_id.date
        self.department_id = self.op_id.department_id
