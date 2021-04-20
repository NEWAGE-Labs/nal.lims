# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from datetime import date

@provider(IFormFieldProvider)
class IInstrumentReads(model.Schema):

    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )
    today = date.datetime.today()

    instrument = schema.TextLine(
        title=u'Instrument',
        required=True,
    )

    start = schema.Datetime(
        title=u'Start',
        required=True,
        default=today,
    )

    end = schema.Datetime(
        title=u'End',
        required=False,
    )
