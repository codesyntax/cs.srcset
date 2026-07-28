# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

try:
    from plone.testing import zope as z2
except ImportError:
    try:
        from plone.testing import z2
    except ImportError:
        z2 = None

import cs.srcset


class CsSrcsetLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.contenttypes
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=plone.app.contenttypes)

        self.loadZCML(package=cs.srcset)

        if z2 is not None:
            z2.installProduct(app, "plone.app.contenttypes")

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.app.contenttypes:default")


CS_SRCSET_FIXTURE = CsSrcsetLayer()


CS_SRCSET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CS_SRCSET_FIXTURE,),
    name="CsSrcsetLayer:IntegrationTesting",
)


CS_SRCSET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CS_SRCSET_FIXTURE,),
    name="CsSrcsetLayer:FunctionalTesting",
)
