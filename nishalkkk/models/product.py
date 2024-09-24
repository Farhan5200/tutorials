from odoo import models, fields


class ProductRatingField(models.Model):
    _inherit = "product.product"

    product_rating = fields.Selection([('0','none'),('1','Poor'),('2','Fair'),('3','Good'),('4','Very Good'),('5','Excellent')],help="Rating of the product")

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('product_rating')
        return result
