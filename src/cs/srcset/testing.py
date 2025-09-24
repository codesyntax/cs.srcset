# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cs.srcset


class CsSrcsetLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)

        self.loadZCML(package=cs.srcset)


CS_SRCSET_FIXTURE = CsSrcsetLayer()


CS_SRCSET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CS_SRCSET_FIXTURE,),
    name="CsSrcsetLayer:IntegrationTesting",
)


CS_SRCSET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CS_SRCSET_FIXTURE,),
    name="CsSrcsetLayer:FunctionalTesting",
)


CS_SRCSET_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CS_SRCSET_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CsSrcsetLayer:AcceptanceTesting",
)
