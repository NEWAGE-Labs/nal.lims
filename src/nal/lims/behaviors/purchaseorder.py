# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.interface import Interface
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.z3cform.widget import SelectFieldWidget
from plone.app.z3cform.widget import DateFieldWidget
from plone.app.z3cform.widget import DatetimeFieldWidget
from nal.lims import POTypes
from bika.lims.browser.widgets import DateTimeWidget

class ILineItemSchema(Interface):

    potype = schema.Choice(
        title=u'item_type',
        vocabulary=POTypes,
        required=False,
        )

    directives.widget(potype=SelectFieldWidget)

    product_number = schema.TextLine(
        title=u'Product Number',
        required=False,
    )

    item_price = schema.Float(
        title=u'Price',
        required=False,
    )


@provider(IFormFieldProvider)
class IPurchaseOrder(model.Schema):

    po_num = schema.TextLine(
        title=u'Purchase Order Number (PO#)',
        required=False,
    )

    details = schema.Text(
        title=u'Order Details',
        required=False,
    )

    total_price = schema.Float(
	title=u'Total Price',
	required=False
    )

    est_arrival = schema.Date(
        title=u'Estimated Arrival',
        required=False,
    )

    received = schema.Date(
        title=u'Received Date',
        required=False,
    )

    directives.widget('est_arrival',DateFieldWidget)
    directives.widget(received=DateFieldWidget)
'''
    line_items = schema.List(
	title = u'Line Items',
	value_type = DictRow(title=u'Table', schema=ILineItemSchema),
	default=[],
	required=False,
   )

    directives.widget(line_items=DataGridFieldFactory)
'''
