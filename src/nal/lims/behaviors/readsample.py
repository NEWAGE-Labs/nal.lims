# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from plone.namedfile import field
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IReadSample(model.Schema):

    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )

    sample = field.NamedFile(
        title=u'CSV of Samples',
        required=False,
    )
