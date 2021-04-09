# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import nal.lims


class NalLimsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=nal.lims)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nal.lims:default')


NAL_LIMS_FIXTURE = NalLimsLayer()


NAL_LIMS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NAL_LIMS_FIXTURE,),
    name='NalLimsLayer:IntegrationTesting',
)


NAL_LIMS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NAL_LIMS_FIXTURE,),
    name='NalLimsLayer:FunctionalTesting',
)


NAL_LIMS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        NAL_LIMS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='NalLimsLayer:AcceptanceTesting',
)
