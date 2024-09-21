

from odoo import api,models

class Demooo(models.Model):
    _name='dem.dem'

    @api.model
    def sales(self,lim):
        return self.env['sale.order'].search_read([],limit=lim)