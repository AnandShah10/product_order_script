# -*- coding: utf-8 -*-
"""Product order to purchase order creation."""

import connection

odoo17_old = connection.getSourceConnection()
odoo17_new = connection.getDestinationConnection()

""" Add x_old_id Field from Script. Write this function before your script's custom function"""


def AddOldId():
    oldIdName = 'x_old_id'
    object_ids = odoo17_new.execute(
        'ir.model', 'search',
        [('model', 'in', ['purchase.order'])])
    print("\n 44444 object_ids :: ", object_ids)
    for object_id in object_ids:
        field = odoo17_new.execute(
            'ir.model.fields', 'search',
            [('model_id', '=', object_id),
             ('name', '=', oldIdName)]
        )
        if not field:
            field_id = odoo17_new.execute(
                'ir.model.fields', 'create',
                {'name': oldIdName,
                 'ttype': 'char',
                 'field_description': 'Old Id',
                 'model_id': object_id,
                 'state': 'manual',
                 'modules': 'purchase'})
            print('55555 Field Created - Old Id - Object:', field_id, object_id)
        else:
            print('66666 Field: %s, Field Already Exist.' % oldIdName, object_id)


AddOldId()


def startMigration():
    purchase_orders = odoo17_old.execute('purchase.order', 'search_read', [])
    partner_id,user_id,company_id,fiscal_position_id,payment_term_id = False,False,False,False,False
    for i, purchase_order in enumerate(purchase_orders):
        partner_id = odoo17_new.execute('res.partner', 'search', [('id', '=', purchase_order.get('partner_id')[0])])
        if partner_id:
            partner_id=partner_id[0]
            print("Partner already exists!!===>", partner_id)
            pass
        else:
            partner_value = \
                odoo17_old.execute('res.partner', 'search_read', [('id', '=', purchase_order.get('partner_id')[0])])[0]
            if partner_value['industry_id']:
                partner_value['industry_id'] = partner_value['industry_id'][0]
            if partner_value.get('user_id', False) and len(partner_value.get('user_id')) > 1:
                partner_value['user_id'] = partner_value['user_id'][0]
            if partner_value['buyer_id'] and len(partner_value.get('buyer_id')) > 1:
                partner_value['buyer_id'] = partner_value['buyer_id'][0]
            if partner_value['parent_id']:
                partner_value['parent_id'] = partner_value['parent_id'][0]
            if partner_value['country_id']:
                partner_value['country_id'] = partner_value['country_id'][0]
            if partner_value['title']:
                partner_value['title'] = partner_value['title'][0]
            if partner_value['team_id']:
                partner_value['team_id'] = partner_value['team_id'][0]
            if partner_value['state_id']:
                partner_value['state_id'] = partner_value['state_id'][0]
            print(partner_value, "value ,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
            old_partner = {
                'name': partner_value['name'],
                'id': partner_value['id'],
                'user_id': partner_value['user_id'],
                'state_id': partner_value['state_id'],
                'country_id': partner_value['country_id'],
                'team_id': partner_value['team_id'],
                'vat': partner_value['vat'],
                'function': partner_value['function'],
                'phone': partner_value['phone'],
                'email': partner_value['email'],
                'website': partner_value['website'],
                'mobile': partner_value['mobile'],
                'buyer_id': partner_value['buyer_id'],
                'active': partner_value['active'],
                'additional_info': partner_value['additional_info'],
                'lang': partner_value['lang'],
                'is_company': partner_value['is_company'],
                'image_1920': partner_value['image_1920'],
                'city': partner_value['city'],
                'color': partner_value['color'],
                'comment': partner_value['comment'],
                'title': partner_value['title'],
                'employee': partner_value['employee'],
                'zip': partner_value['zip'],
                'ref': partner_value['ref'],
            }
            partner_id = odoo17_new.execute('res.partner', 'create', old_partner)
            print("Partner created!===>", partner_id)

        user_id = odoo17_new.execute('res.users', 'search', [('id', '=', purchase_order.get('user_id')[0])])
        if user_id:
            user_id=user_id[0]
            print("User already exists!!===>", user_id)
            pass
        else:
            user_value = \
                odoo17_old.execute('res.users', 'search_read', [('id', '=', purchase_order.get('user_id')[0])])[0]
            print("User Value......................", user_value)
            old_user = {
                'id': user_value['id'],
                'login': user_value['login'],
                'active': user_value['active'],
                'lang': user_value['lang'],
                'image_1920': user_value['image_1920'],
                'color': user_value['color'],
                'comment': user_value['comment'],
                'notification_type': user_value['notification_type'],
                'name': user_value['name']
            }
            user_id = odoo17_new.execute('res.users', 'create', old_user)
            print("User created!====>", user_id)

        company_id = odoo17_new.execute('res.company', 'search', [('id', '=', purchase_order.get('company_id')[0])])
        if company_id:
            company_id=company_id[0]
            print("Company already exists!!===>", company_id)
            pass
        else:
            company_value = \
                odoo17_old.execute('res.company', 'search_read', [('id', '=', purchase_order.get('company_id')[0])])[0]
            company_id = odoo17_new.execute('res.company', 'create', company_value)
            print("Company created!=====>", company_id)

        if purchase_order.get('payment_term_id'):
            payment_term_id = odoo17_new.execute('account.payment.term', 'search',
                                                 [('id', '=', purchase_order.get('payment_term_id')[0])])
            if payment_term_id:
                payment_term_id=payment_term_id[0]
                print("Payment Term Already Exists!=====>", payment_term_id)
                pass
            else:
                term_value = \
                    odoo17_old.execute('account.payment.term', 'search_read',
                                       [('id', '=', purchase_order.get('payment_term_id')[0])])[0]
                print(term_value, 'Term jjjjjjjjjjjjjjjjjjjjjjjjjj')
                old_term = {
                    'id': term_value['id'],
                    'name': term_value['name'],
                    'note': term_value['note'],
                    'sequence': term_value['sequence'],
                    'active': term_value['active'],
                    'discount_days': term_value['discount_days'],
                    'discount_percentage': term_value['discount_percentage'],
                    'display_on_invoice': term_value['display_on_invoice'],
                    'early_discount': term_value['early_discount'],
                    'early_pay_discount_computation': term_value['early_pay_discount_computation'],
                    'company_id': term_value['company_id'][0] if term_value['company_id'] and len(
                        term_value['company_id']) > 1 else term_value['company_id'],
                    'currency_id': term_value['currency_id'][0] if term_value['currency_id'] and len(
                        term_value['currency_id']) > 1 else term_value['currency_id']

                }
                if term_value['line_ids']:
                    term_lines = odoo17_old.execute('account.payment.term.line', 'search_read',
                                                    [('payment_id', '=', term_value.get('id'))])
                    print("term_lines########################",term_lines)
                    # del term_value['line_ids']
                else:
                    term_lines = []
                payment_term_id = odoo17_new.execute('account.payment.term', 'create', old_term)
                if term_lines:
                    for term in term_lines:
                        term['payment_id'] = payment_term_id
                        del term['create_uid'],term['write_uid']
                        print("Term line >>>>>>>>>>>>>>>>>>>", term)
                        odoo17_new.execute('account.payment.term.line', 'create', term)
                print("Payment Term created!=====>", payment_term_id)

        if purchase_order.get('fiscal_position_id'):
            fiscal_position_id = odoo17_new.execute('account.fiscal.position', 'search',
                                                    [('id', '=', purchase_order.get('fiscal_position_id')[0])])
            if fiscal_position_id:
                fiscal_position_id=fiscal_position_id[0]
                print("Fiscal Position Already Exists!=====>", fiscal_position_id)
                pass
            else:
                fiscal_value = \
                    odoo17_old.execute('account.fiscal.position', 'search_read',
                                       [('id', '=', purchase_order.get('fiscal_position_id')[0])])[0]
                old_fiscal={
                    'name':fiscal_value['name'],
                    'active':fiscal_value['active'],
                    'note':fiscal_value['note'],
                    'vat_required':fiscal_value['vat_required'],
                    'auto_apply':fiscal_value['auto_apply'],
                    'zip_from':fiscal_value['zip_from'],
                    'zip_to':fiscal_value['zip_to'],
                    'foreign_vat':fiscal_value['foreign_vat'],
                    'id':fiscal_value['id'],
                    'sequence':fiscal_value['sequence'],
                    'country_id': fiscal_value['country_id'][0] if fiscal_value['country_id'] and len(
                        fiscal_value['country_id']) > 1 else fiscal_value['country_id'],
                }
                fiscal_position_id = odoo17_new.execute('account.fiscal.position', 'create', old_fiscal)
                print("Payment Term created!=====>", fiscal_position_id)

        order_lines = odoo17_old.execute('purchase.order.line', 'search_read',
                                         [('order_id', '=', purchase_order.get('id'))])
        print("oReder lines tryfugihfvuihruidheihuiduiihiiei",user_id,partner_id,fiscal_position_id,company_id)
        record = odoo17_new.execute('purchase.order', 'create', {
            # 'partner_id': purchase_order.get('partner_id')[0] if purchase_order.get('partner_id') and len(
            #     purchase_order.get('partner_id')) > 1 else purchase_order.get('partner_id'),
            'partner_id':partner_id,
            'date_order': purchase_order.get('date_order', False),
            # 'payment_term_id': purchase_order.get('payment_term_id')[0] if purchase_order.get(
            #     'payment_term_id') and len(purchase_order.get('payment_term_id')) > 1 else purchase_order.get(
            #     'payment_term_id', False),
            'payment_term_id':payment_term_id,
            # 'user_id': purchase_order.get('user_id')[0] if purchase_order.get('user_id') and len(
            #     purchase_order.get('user_id')) > 1 else purchase_order.get('user_id', False),
            'user_id':user_id,
            # 'fiscal_position_id': purchase_order.get('fiscal_position_id')[0] if purchase_order.get(
            #     'fiscal_position_id') and len(purchase_order.get('fiscal_position_id')) > 1 else purchase_order.get(
            #     'fiscal_position_id', False),
            'fiscal_position_id':fiscal_position_id,
            'amount_tax': purchase_order.get('amount_tax'),
            'amount_total': purchase_order.get('amount_total'),
            'amount_untaxed': purchase_order.get('amount_untaxed'),
            # 'company_id': purchase_order.get('company_id')[0] if purchase_order.get('company_id') and len(
            #     purchase_order.get('company_id')) > 1 else purchase_order.get('company_id', False),
            'company_id':company_id,
            'notes': purchase_order.get('notes', False),
            'create_date': purchase_order.get('create_date'),
            'name': purchase_order.get('name'),
            'origin': purchase_order.get('origin', False),
            'priority': purchase_order.get('priority', False),
            'write_date': purchase_order.get('write_date'),
            'date_approve': purchase_order.get('date_approve', False),
            'state': purchase_order.get('state'),
            'partner_ref': purchase_order.get('partner_ref', False),
            # 'incoterm_id': purchase_order.get('incoterm_id')[0] if purchase_order.get('incoterm_id') and len(
            #     purchase_order.get('user_id')) > 1 else purchase_order.get('incoterm_id', False),
            'x_test_m2m_field': purchase_order.get('x_test_m2m_field'),
            'x_old_id': purchase_order.get('id'),
        })
        print("Record Created!!=====>", record)
        for j in order_lines:
            if j['taxes_id']:
                for tax_id in j['taxes_id']:
                    tax_val = odoo17_new.execute('account.tax', 'search', [('id', '=', tax_id)])
                    if tax_val:
                        print("Tax Exists===>", tax_val)
                    else:
                        old_tax = odoo17_old.execute('account.tax', 'search_read', [('id', '=', tax_id)])[0]
                        print(old_tax, "Old Taxjjjjjjjjjjjjjjjjjjjjjjjj")
                        old_tax_value = {
                            'name': old_tax['name'],
                            'sequence': old_tax['sequence'],
                            'tax_exigibility': old_tax['tax_exigibility'],
                            'active': old_tax['active'],
                            'amount': old_tax['amount'],
                            'amount_type': old_tax['amount_type'],
                            'analytic': old_tax['analytic'],
                            'tax_scope': old_tax['tax_scope'],
                            'type_tax_use': old_tax['type_tax_use'],
                            'price_include': old_tax['price_include'],
                            'is_base_affected': old_tax['is_base_affected'],
                            'id': old_tax['id'],
                            'invoice_label': old_tax['invoice_label'],
                            'include_base_amount': old_tax['include_base_amount'],
                            'description': old_tax['description'],
                            'country_id': old_tax['country_id'][0] if old_tax['country_id'] and len(
                                old_tax['country_id']) > 1 else old_tax['country_id'],
                        }
                        tax = odoo17_new.execute('account.tax', 'create', old_tax_value)
                        print("Tax created!========>", tax)
            value = {
                'order_id': record,
                'product_id': j['product_id'][0],
                'product_qty': j['product_qty'],
                'price_unit': j['price_unit'],
                'taxes_id': j['taxes_id']
            }
            odoo17_new.execute('purchase.order.line', 'create', value)


startMigration()
