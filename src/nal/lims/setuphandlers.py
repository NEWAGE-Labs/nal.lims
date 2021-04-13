# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from bika.lims import api
from zope.interface import implementer

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'nal.lims:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    nallims = api.get_portal()

    #Change 'Batches' folder title to 'SDGs'
    nallims.batches.title = "SDGs"
    #Change 'Batch Labels' folder to 'SDG Labels'
    nallims.bika_setup.bika_batchlabels.title = "SDG Labels"

def uninstall(context):
    """Uninstall script"""
    #Do something at the end of the uninstallation of this package.
    nallims = api.get_portal()

    #Revert 'Batches' folder to default senaite title
    nallims.batches.title = "Batches"
    #Revert 'Batch Labels' folder to default senaite title
    nallims.bika_setup.bika_batchlabels.title = "Batch Labels"
