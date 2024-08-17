# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    """used to create student registration form"""
    _name = "student.registration"
    _description = "Student Registration"
    _inherit = 'mail.thread'

    first_name = fields.Char("First Name", required=True, tracking=True)
    last_name = fields.Char("Last Name", tracking=True)
    father = fields.Char("Father")
    mother = fields.Char("Mother", tracking=True)
    same_as_communication = fields.Boolean("Same as above", tracking=True)
    email = fields.Char("Email", required=True, tracking=True)
    Phone = fields.Char("Phone", required=True, tracking=True)
    date_of_birth = fields.Date("DOB", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], tracking=True)
    registration_date = fields.Date("Registration Date", default=fields.Datetime.now(), tracking=True)
    photo = fields.Image("Photo")
    previous_academic_department_id = fields.Many2one("school.department",
                                                      string="Previous Academic Department", tracking=True)
    previous_class_id = fields.Many2one("school.class", string="Previous class", tracking=True)
    file = fields.Binary("TC")
    filename = fields.Char()
    aadhaar_number = fields.Char("Aadhaar Number", copy=False, tracking=True)
    name = fields.Char("Student no", required=True, default=lambda self: _('New'), copy=False, readonly=True,
                       tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('registration', 'Registration')
    ], default='draft', tracking=True, copy=False)
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company)
    age = fields.Integer("Age", tracking=True, compute="_compute_calculate_age", store=True)
    """fields for communication address"""
    c_street = fields.Char(required=True, tracking=True)
    c_street2 = fields.Char()
    c_city = fields.Char(required=True)
    c_zip = fields.Char()
    c_state_id = fields.Many2one("res.country.state")
    c_country_id = fields.Many2one("res.country", required=True)
    """fields for permanent address"""
    p_street = fields.Char(required=True, tracking=True)
    p_street2 = fields.Char()
    p_city = fields.Char(required=True)
    p_zip = fields.Char()
    p_state_id = fields.Many2one("res.country.state")
    p_country_id = fields.Many2one("res.country", required=True)
    club_id = fields.Many2many("school.club", string="Club")
    _sql_constraints = [
        ('aadhaar_number_uniq', 'unique(aadhaar_number)', "A aadhaar number can only be assigned to one student !")]

    def action_button_confirm(self):
        """works when clicking the confirm button"""
        self.write({
            'status': 'registration',
        })
        if not self.gender:
            raise ValidationError("Gender details are required")
        if not self.date_of_birth:
            raise ValidationError("Date of birth is required")
        if self.status == 'registration':
            self.write({
                'name': self.env['ir.sequence'].next_by_code('student.reference'),
            })

    @api.depends('date_of_birth')
    def _compute_calculate_age(self):
        """to calculate age based on date of birth"""
        dob_date = 0
        if self.date_of_birth:
            dob_date = self.date_of_birth
        today_date = datetime.today()
        age = relativedelta(today_date, dob_date).years
        self.age = age

    @api.constrains('age')
    def _check_age(self):
        """to check whether the age is greater than 0"""
        for rec in self:
            if rec.date_of_birth:
                if rec.age < 5:
                    raise ValidationError('Age should be greater than 4...!')

    @api.onchange('same_as_communication', 'c_street', 'c_street2', 'c_city', 'c_zip', 'c_state_id', 'c_country_id')
    def permanent_address(self):
        """for populating permanent address"""
        if self.same_as_communication:
            self.write({
                'p_street': self.c_street,
                'p_street2': self.c_street2,
                'p_city': self.c_city,
                'p_zip': self.c_zip,
                'p_state_id': self.c_state_id,
                'p_country_id': self.c_country_id
            })
        else:
            self.write({
                'p_street': "",
                'p_street2': "",
                'p_city': "",
                'p_zip': "",
                'p_state_id': "",
                'p_country_id': ""
            })

    @api.constrains('file', 'filename')
    def _check_pdf_file(self):
        """to check whether the uploaded file is pdf or not"""
        if self.file:
            if not self.filename.endswith('.pdf'):
                raise ValidationError('Only pdf format is supported')
            else:
                pass
