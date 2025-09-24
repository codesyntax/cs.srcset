# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cs.srcset.testing import CS_SRCSET_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that cs.srcset is properly installed."""

    layer = CS_SRCSET_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cs.srcset is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'cs.srcset'))

    def test_browserlayer(self):
        """Test that ICsSrcsetLayer is registered."""
        from cs.srcset.interfaces import ICsSrcsetLayer
        from plone.browserlayer import utils
        self.assertIn(
            ICsSrcsetLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CS_SRCSET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('cs.srcset')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if cs.srcset is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'cs.srcset'))

    def test_browserlayer_removed(self):
        """Test that ICsSrcsetLayer is removed."""
        from cs.srcset.interfaces import ICsSrcsetLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICsSrcsetLayer, utils.registered_layers())
