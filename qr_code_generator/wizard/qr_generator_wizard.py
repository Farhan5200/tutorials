# -*- coding: utf-8 -*-

from odoo import api,models, fields
import qrcode
import base64
from io import BytesIO
from odoo.http import request



class QrGenerator(models.TransientModel):
    _name = 'qr.generator.wizard'
    _description = 'QR Code Generator'

    text_box = fields.Char()
    qr_code = fields.Binary("QR Code", compute='generate_qr_code')

    @api.onchange('text_box')
    def generate_qr_code(self):
        print('hi')
        for rec in self:
             qr = qrcode.QRCode(
                 version=1,
                 error_correction=qrcode.constants.ERROR_CORRECT_L,
                 box_size=3,
                 border=4,
             )
             qr.add_data("Text : ")
             qr.add_data(rec.text_box)
             qr.make(fit=True)
             img = qr.make_image()
             temp = BytesIO()
             img.save(temp, format="PNG")
             qr_image = base64.b64encode(temp.getvalue())
             rec.update({'qr_code': qr_image})

    def reset(self):
       return request.render('school_management.events_data_website_template')