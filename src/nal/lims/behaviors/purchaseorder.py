# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.interface import Interface
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.z3cform.widget import SelectFieldWidget

class ILineItemSchema(Interface):

    choice_field = schema.Choice(
        title=u'Choice Field',
        vocabulary='nal.lims.vocabularies.POTypes',
        required=False,
        )

    directives.widget('objective', SelectFieldWidget)

    product_number = schema.TextLine(
        title=u'Textline field',
        required=False,
    )

    item_price = schema.Integer(
        title=u'Price',
        required=False,
    )


@provider(IFormFieldProvider)
class IPurchaseOrder(model.Schema):

    po_num = schema.TextLine(
        title=u'Purchase Order Number (PO#)',
        required=False,
    )

    total_price = schema.Integer(
	title=u'Total Price',
	required=False
    )

    est_arrival = schema.Datetime(
        title=u'Estimated Arrival',
        required=False,
    )

    received = schema.Datetime(
        title=u'Received Date',
        required=False,
    )

    line_items = schema.List(
	title = 'Line Items',
	value_type = DictRow(title=u'Table', schema=ILineItemSchema),
	default=[],
	required=False,
    )

    directives.widget('datagrid_field', DataGridFieldFactory)
