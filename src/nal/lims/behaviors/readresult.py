# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IReadResult(model.Schema):

    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )

    analyte = schema.TextLine(
        title=u'Analyte',
        required=False,
    )

    result = schema.Float(
        title=u'Result',
        required=False,
    )
