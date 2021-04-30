# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from datetime import date
from plone.namedfile import field

@provider(IFormFieldProvider)
class IInstrumentReadFolder(model.Schema):
    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )
    sample = field.NamedFile(
        title=u'CSV of Samples',
        required=False,
    )
