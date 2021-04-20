# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IInstrumentResult(model.Schema):

    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )

    sample = schema.TextLine(
        title=u'Sample Name',
        required=False,
    )

    analyte = schema.TextLine(
        title=u'Analyte',
        required=False,
    )

    result = schema.Float(
        title=u'Result',
        required=False,
    )
