# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class OpTicket(models.Model):
    _name = "op.ticket"
    _description = "Op Ticket"

    name = fields.Char("OP Number", required=True, default=lambda self: _('New'), copy=False, readonly=True,
                       tracking=True)
    date = fields.Date("Date", default=fields.datetime.now())
    token_number = fields.Integer("Token No:", required=True)
    patient_id = fields.Many2one('res.partner', string="Patient", required=True)
    doctor_id = fields.Many2one("hr.employee", string="Doctor", required=True)
    patient_age = fields.Integer("Patient Age", required=True)
    department_id = fields.Many2one("hr.department", string="Department", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm')
    ], default="draft")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'op.reference')
        return super().create(vals_list)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.patient_age = self.patient_id.age or 0

    @api.onchange('doctor_id')
    def onchange_doctor_id(self):
        self.department_id = self.doctor_id.department_id

    def button_confirm(self):
        self.write({
            'state': 'confirm'
        })
