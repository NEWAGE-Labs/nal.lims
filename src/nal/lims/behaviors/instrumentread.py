# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IInstrumentRead(model.Schema):

    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )

    instrument = schema.TextLine(
        title=u'Instrument',
        required=False,
    )

    start = schema.Datetime(
        title=u'Start of Read',
        required=False,
    )

    end = schema.Datetime(
        title=u'End of Read',
        required=False,
    )
