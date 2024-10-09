# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.interface import Interface
from plone.app.z3cform.widget import SelectFieldWidget
from plone.app.z3cform.widget import DateFieldWidget
from plone.app.z3cform.widget import DatetimeFieldWidget
from senaite.core.z3cform.widgets.datetimewidget import DatetimeWidget
from senaite.core.z3cform.widgets.datagrid import DataGridWidgetFactory
from senaite.core.schema import DatetimeField
from senaite.core.schema.fields import DataGridField
from senaite.core.schema.fields import DataGridRow
from senaite.core.api import dtime
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

    quantity = schema.Int(
        title=u'Quantity',
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

    est_arrival = DatetimeField(
        title=u'Estimated Arrival',
        description=u"Date the Purchase Order is estimated to arrive at the lab.",
        required=False,
    )

    received = DatetimeField(
        title=u'Received Date',
        description=u"Date the Purchase Order was received by the lab.",
        required=False,
    )

    directives.widget("est_arrival",DatetimeWidget,show_time=False)
    directives.widget("received",DatetimeWidget,show_time=False)


    line_items = DataGridField(
	title = u'Line Items',
	description = u'The individual items purchased as part of the order.',
	value_type = DataGridRow(title=u'Table', schema=ILineItemSchema),
	default=[],
	missing_value=[],
	required=False,
   )

    directives.widget("line_items",DataGridWidgetFactory, allow_reorder=True, auto_append=True)
