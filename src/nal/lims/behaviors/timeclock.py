# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class ITimeclock(model.Schema):

    # directives.fieldset(
    #     'metrc',
    #     label=u'METRC',
    #     fields=('rfid','room', 'cannabis'),
    # )

    personnel = schema.TextLine(
        title=u'Personnel',
        required=False,
    )

    type = schema.TextLine(
        title=u'Type',
        required=False,
    )

    hours = schema.Int(
        title=u'Hours',
        required=False,
    )
