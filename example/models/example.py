# -*- coding: utf-8 -*-
from audioop import reverse

from odoo import fields, models


class Example(models.Model):
    """ To learn relation type fields"""
    _name = 'example'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    line_ids = fields.One2many('example.line', 'example_id')
    tag_ids = fields.Many2many('example.tag')

    def action_button(self):
        """To perform x2many value filling concept"""
        print("helloo")
        limit= [0,0]
        # sum = 0
        quantity = 0
        # for rec in self.line_ids.filtered(lambda x:x.quantity >= 10):
        #     # if rec.quantity >= 10:
        #        limit[0] += rec.price
        #        limit[1] += rec.quantity
        # 
        # # limit.append(sum)
        # # limit.append(quantity)
        # 
        # hii = self.line_ids.filtered(lambda x:x.quantity >= 10).sorted('quantity').mapped('quantity')
        # print(hii)
        # print(sum(hii))
        print(self.line_ids.search([('quantity', '>=', 10)]))
        print(self.line_ids.filtered(lambda x:x.quantity >= 10))


        # product_id = self.env['product.product'].search([], order='id desc', limit=1)
        # print(product_id.name)
        # # fields.Command.create(values)
        # first Method
        # self.line_ids = [fields.Command.create({
        #     'product_id': product_id.id,
        #     'price': product_id.lst_price,
        #     'quantity': 5
        # })]

        # self.write({
        #     'line_ids': [fields.Command.create({
        #         'product_id': product_id.id,
        #         'price': product_id.lst_price,
        #         'quantity': 5
        #     })]
        # })

        # self.line_ids.create({
        #     'product_id': product_id.id,
        #     'price': product_id.lst_price,
        #     'quantity': 5,
        #     'example_id' : self.id
        # })

        # fields.Command.update(id,values)
        line_id = self.line_ids[-1]
        # self.line_ids = [fields.Command.update(line_id.id,{
        #     # 'product_id': product_id.id,
        #     # 'price': product_id.lst_price,
        #     'quantity': 10
        # })]
        #
        # line_id.write({
        #     'quantity': 10,
        # })
        # fields.Command.delete(id)
        # self.line_ids = [fields.Command.delete(line_id.id)]
        #
        # line_id.unlink()
        # fields.Command.create(values)
        # first Method
        # self.line_ids = [fields.Command.create({
        #     'product_id': product_id.id,
        #     'price': product_id.lst_price,
        #     'quantity': 5
        # })]

        # self.write({
        #     'line_ids': [fields.Command.create({
        #         'product_id': product_id.id,
        #         'price': product_id.lst_price,
        #         'quantity': 5
        #     })]
        # })

        # self.line_ids.create({
        #     'product_id': product_id.id,
        #     'price': product_id.lst_price,
        #     'quantity': 5,
        #     'example_id' : self.id
        # })

        # # fields.Command.link(id)
        # tag_id = self.tag_ids.search([('name','=','new')],limit=1)
        # self.tag_ids = [fields.Command.link(tag_id.id)]

        empty_line_id = self.line_ids.search([('example_id','=',False),('example_example_id','=',False)])
        # print("aaaa",empty_line_id.product_id.name)
        # self.line_ids =[fields.Command.unlink(self.line_ids[-1].id)]

        # fields.Command.clear()
        # self.line_ids =[fields.Command.clear()]

        # fields.Command.set(ids)
        # self.line_ids = [fields.Command.set(empty_line_id.ids)]


        #
        # fields.Command.unlink(id)
        # tag_id = self.tag_ids.search([('name', '=', 'new')], limit=1)
        # self.tag_ids = [fields.Command.unlink(tag_id.id)]

class ExampleLine(models.Model):
    """ To learn one2many"""
    _name = 'example.line'

    example_id = fields.Many2one('example')
    example_example_id = fields.Many2one('example.example')
    product_id = fields.Many2one('product.product')
    price = fields.Float()
    quantity = fields.Float()


class ExampleTag(models.Model):
    """ To learn many2many"""

    _name = 'example.tag'

    name = fields.Char()
