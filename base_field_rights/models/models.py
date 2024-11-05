# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.osv import expression
from odoo.exceptions import AccessError
from odoo.http import request
import logging

from odoo import api, fields, models, SUPERUSER_ID, tools, _

import functools
from operator import attrgetter
from collections import defaultdict
from lxml import etree

import logging


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def get_fields_restricted(self):
        cr = self._cr
        cr.execute("""
            (
                SELECT
                    f1.*
                FROM
                    ir_model_fields as f1
                    join ir_model_fields_group_rel as b on f1.id = b.field_id and f1.model = '%s'
            )
            union
            (
                SELECT
                    f2.*
                FROM
                    ir_model_fields as f2
                    join ir_model_field_access as c on f2.id = c.field_id and f2.model = '%s'
            )
        
         """ % (self._name, self._name))
        result = defaultdict(dict)

        for row in cr.dictfetchall():
            result[row['model']][row['name']] = row

        return result

    def get_field_access_list(self, field_id):
        cr = self._cr
        cr.execute("""
                 (select
                        rel.group_id
                    from
                        ir_model_fields_group_rel as rel
                    where
                        rel.field_id = '%s')
            union
            (
                select
                        acl.group_id
                    from
                        ir_model_field_access as acl
                    where
                        acl.field_id = '%s' and perm_write = true
            )
         """ % (field_id, field_id))
        full_access_group_ids = [row['group_id'] for row in cr.dictfetchall()]

        cr.execute("""
                select
                        acl.group_id
                    from
                        ir_model_field_access as acl
                    where
                        acl.field_id = '%s' and perm_read = true and perm_write != true
        
         """ % (field_id))

        partial_access_group_ids = [row['group_id'] for row in cr.dictfetchall()]

        cr.execute("""
                select
                        acl.group_id
                    from
                        ir_model_field_access as acl
                    where
                        acl.field_id = '%s' and perm_read != true and perm_write != true
        
         """ % (field_id))

        no_access_group_ids = [row['group_id'] for row in cr.dictfetchall()]

        return {'readWrite': full_access_group_ids, 'readOnly': partial_access_group_ids, 'invisible': no_access_group_ids}

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """ fields_get([fields][, attributes])

        Return the definition of each field.

        The returned value is a dictionary (indexed by field name) of
        dictionaries. The _inherits'd fields are included. The string, help,
        and selection (if present) attributes are translated.

        :param allfields: list of fields to document, all if empty or not provided
        :param attributes: list of description attributes to return for each field, all if empty or not provided
        """
        from odoo.http import request
        has_access = functools.partial(self.check_access_rights, raise_exception=False)
        readonly = not (has_access('write') or has_access('create'))

        res = {}
        fields_restricted = self.get_fields_restricted()

        for fname, field in self._fields.items():
            x_readonly = False
            x_invisible = False

            if allfields and fname not in allfields:
                continue
            if field.groups and not self.env.su and not self.user_has_groups(field.groups):
                continue

            if field.name in fields_restricted[self._name]:
                field_id = fields_restricted[self._name][field.name]['id']
                assert field_id, 'not found field_id'

                access_list = self.get_field_access_list(field_id)
                user_group_ids = self.env['res.users'].search([('id', '=', self.env.uid)]).groups_id.ids
                # 判断模式从 “白名单” 改为 ”黑名单“
                # 黑名单模式：
                # 不在 字段 ACL 里面的用户，拥有全部的权限
                # 在 字段 ACL 里面的用户， 根据 ACL 授予权限
                # 白名单模式
                # 在 字段 ACL 里面的用户，才拥有 ACL 指定的权限
                # 其他不在 ACL 里面的用户， 将不拥有 任何权限
                # 原始 白名单代码 如下
                #
                # in_readWrite = list(
                #     set(user_group_ids) & set(access_list['readWrite']))
                # in_readOnly = list(
                #     set(user_group_ids) & set(access_list['readOnly']))
                #
                # if not self.env.su and not any(in_readWrite + in_readOnly):
                #     x_invisible = True
                #
                # if not in_readWrite:
                #     x_readonly = True

                if list(set(user_group_ids) & set(access_list['invisible'])):
                    x_invisible = True

                if list(set(user_group_ids) & set(access_list['readOnly'])):
                    x_invisible = False
                    x_readonly = True

                if list(set(user_group_ids) & set(access_list['readWrite'])):
                    x_invisible = False
                    x_readonly = False

            description = field.get_description(self.env)
            if readonly:
                description['readonly'] = True
                description['states'] = {}
            else:
                if x_readonly:
                    description['readonly'] = True
                    description.update({'force-readonly': True})

            if x_invisible:
                description['invisible'] = True
                description.update({'force-invisible': True})

            if attributes:
                description = {key: val for key, val in description.items() if key in attributes}
            res[fname] = description

        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        fv = super(BaseModel, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        doc = etree.XML(fv['arch'])
        tag_fields = doc.xpath('//field')
        fields_name = []

        for tag_field in tag_fields:
            fields_name.append(tag_field.get('name'))

        field_defs = self.fields_get(allfields=fields_name)

        for field_name in field_defs:
            field_description = field_defs[field_name]

            if field_description.get('force-readonly', False):
                for node in doc.xpath("//field[@name='%s']" % field_name):
                    modifiers = node.get('modifiers')
                    node.set('modifiers', '{"readonly": true}')

            if field_description.get('force-invisible', False):
                for node in doc.xpath("//field[@name='%s']" % field_name):
                    node.set('modifiers', '{"invisible": true}')

        fv['arch'] = etree.tostring(doc, encoding='unicode')
        return fv


reserved_fields = [
    # magic
    '__last_update',
    'active',
    'company_id',
    'create_date',
    'create_uid',
    'id',
    'name',
    'state',
    'write_date',
    'write_uid',
    # mail thread
    'message_attachment_count',
    'message_channel_ids',
    'message_follower_ids',
    'message_has_error_counter',
    'message_has_error',
    'message_ids',
    'message_is_follower',
    'message_main_attachment_id',
    'message_needaction_counter',
    'message_needaction',
    'message_partner_ids',
    'message_unread_counter',
    'message_unread',
    # activity
    'activity_date_deadline',
    'activity_exception_decoration',
    'activity_exception_icon',
    'activity_ids',
    'activity_state',
    'activity_summary',
    'activity_type_id',
    'activity_user_id',
    # Tier Validation
    'approve_state',
    'can_forward'
    'can_review',
    'disable_withdraw',
    'has_comment',
    'is_current_uid',
    'is_member_of_audit_group',
    'need_validation',
    'rejected',
    'review_ids',
    'reviewer_ids',
    'reviewer_names',
    'reviewer_time',
    'validated',
]


class IrModelFieldAccess(models.Model):
    _name = 'ir.model.field.access'
    _description = 'Model Field Access'
    _order = 'model_id,field_id,group_id,name,id'

    name = fields.Char(required=True, index=True)
    active = fields.Boolean(
        default=True,
        help=
        'If you uncheck the active field, it will disable the ACL without deleting it (if you delete a native ACL, it will be re-created when you reload the module).'
    )
    model_id = fields.Many2one('ir.model',
                               string='Object',
                               required=False,
                               domain=[('transient', '=', False)],
                               index=True,
                               ondelete='cascade',
                               related='field_id.model_id',
                               store=True)
    field_id = fields.Many2one('ir.model.fields', string='Field', required=True, domain=[('model_id', '=', 'model_id')], index=True, ondelete='cascade')
    group_id = fields.Many2one('res.groups', string='Group', ondelete='cascade', index=True)
    perm_read = fields.Boolean(string='Read Access')
    perm_write = fields.Boolean(string='Write Access')

    field_description = fields.Char(related='field_id.field_description')

    @api.model
    def check_groups(self, group):
        """ Check whether the current user has the given group. """
        grouparr = group.split('.')
        if not grouparr:
            return False
        self._cr.execute(
            """SELECT 1 FROM res_groups_users_rel
                            WHERE uid=%s AND gid IN (
                                SELECT res_id FROM ir_model_data WHERE module=%s AND name=%s)""", (
                self._uid,
                grouparr[0],
                grouparr[1],
            ))
        return bool(self._cr.fetchone())

    @api.model
    def check_group(self, field, mode, group_ids):
        """ Check if a specific group has the access mode to the specified field"""
        assert mode in ('read', 'write'), 'Invalid access mode'

        if isinstance(field, models.BaseModel):
            assert field._name == 'ir.model.fields', 'Invalid field object'
            field_name = field.name
        else:
            field_name = field

        if isinstance(group_ids, int):
            group_ids = [group_ids]

        query = """ SELECT 1 FROM ir_model_field_access a
                    JOIN ir_model_fileds f ON (f.id = a.field_id)
                    WHERE a.active AND a.perm_{mode} AND
                        f.name=%s AND (a.group_id IN %s OR a.group_id IS NULL)
                """.format(mode=mode)
        self._cr.execute(query, (field_name, tuple(group_ids)))
        return bool(self._cr.rowcount)


class IrModel(models.Model):
    _inherit = 'ir.model'

    field_access_ids = fields.One2many('ir.model.field.access', 'model_id', string='Field Access')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = self.__force_domain(domain)

        return super(IrModel, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):

        args = self.__force_domain(args)

        return super(IrModel, self).name_search(name=name, args=args, operator=operator, limit=limit)

    def __force_domain(self, domain):
        role_id = self.env.context.get('role_id', False)
        model_ids = []
        if role_id:
            role = self.sudo().env['res.users.role'].with_context({'lang': 'en_US'}).search([('id', '=', role_id)])

            for menu_line in role.menu_line_ids:
                model_ids.append(menu_line.model_id.id)

        if model_ids:
            domain = expression.AND([[('id', 'in', model_ids)], domain])

        return domain

    @api.model
    def get_model_fields(self, model_ids):
        """返回指定模型的字段列表

        Args:
            model_ids (list): 模型列表

        Returns:
            dict: 模型的字段列表， 字段以dict 表示
        """
        data = {}
        if not model_ids:
            return data
        for model in self.search([('id', 'in', model_ids)], order='name'):
            fields_in_form = self.sudo().env[model.model].fields_get_form(None)
            for key in reserved_fields:
                fields_in_form.pop(key, 'key_not_found')
            model_data = [{
                'id': field.id,
                'name': field.name,
                'description': field.field_description
            } for field in model.field_id if field.name in fields_in_form]
            model_data = sorted(model_data, key=lambda x: x['description'])
            data.update({model.model: model_data})

        return data


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    access_ids = fields.One2many('ir.model.field.access', 'field_id', string='Access')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = self.__force_domain(domain)

        return super(IrModelFields, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):

        args = self.__force_domain(args)

        return super(IrModelFields, self).name_search(name=name, args=args, operator=operator, limit=limit)

    def __force_domain(self, domain):
        model_id = self.env.context.get('model_id', False)
        if self.env.context.get('onscreen', False) and model_id:
            model_obj = self.sudo().env['ir.model'].with_context({'lang': 'en_US'}).search([('id', '=', model_id)])

            Model = self.env[model_obj.model]
            fields_onscreen = Model.sudo().fields_get_form(None)
            onscreen_ids = []

            def _remove_reserved_field(fields):
                reserved_fields = ['id', 'name', 'active', 'company_id', 'create_uid', 'create_date', 'write_uid', 'write_date']

                try:
                    for res in reserved_fields:
                        fields.pop(res)
                except KeyError:
                    pass

                return fields

            fields_onscreen = _remove_reserved_field(fields_onscreen)

            for field in model_obj.field_id:
                if field.name in fields_onscreen:
                    onscreen_ids.append(field.id)

            domain = expression.AND([[('id', 'in', onscreen_ids)], domain])

        return domain
