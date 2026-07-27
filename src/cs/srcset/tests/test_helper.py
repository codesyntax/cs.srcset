import unittest
from cs.srcset.testing import CS_SRCSET_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedImage
from plone.namedfile.tests import getFile


from plone.supermodel import model
from plone.namedfile import field as namedfile

class ICustomImage(model.Schema):
    photo = namedfile.NamedImage(title="Photo", required=False)
    logo = namedfile.NamedImage(title="Logo", required=False)


class TestImageHelper(unittest.TestCase):

    layer = CS_SRCSET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a News Item
        self.portal.invokeFactory("News Item", "news1", title="News 1")
        self.news1 = self.portal.news1
        
        # Add an image to the news item
        image_data = getFile("image.png")
        self.news1.image = NamedImage(image_data, "image/png", "image.png")
        self.news1.reindexObject()
        
        # Get the helper view
        self.helper = api.content.get_view("image_helper", self.portal, self.request)

    def test_news_item_srcset_brain(self):
        """Test srcset with a News Item brain."""
        brains = api.content.find(id="news1")
        self.assertEqual(len(brains), 1)
        brain = brains[0]
        
        # Verify image_scales metadata is present
        self.assertTrue(hasattr(brain, "image_scales"))
        self.assertIn("image", brain.image_scales)
        
        tag = self.helper.srcset(brain, fieldname="image", sizes="50vw", css_class="my-news-img")
        
        # Assertions on generated tag
        self.assertIn('src="http://nohost/plone/news1/@@images/image', tag)
        self.assertIn('srcset="', tag)
        self.assertIn('sizes="50vw"', tag)
        self.assertIn('class="my-news-img"', tag)
        self.assertIn('alt="News 1"', tag)
        self.assertIn('loading="lazy"', tag)

    def test_news_item_srcset_object(self):
        """Test srcset with a News Item object (fallback path)."""
        tag = self.helper.srcset(self.news1, fieldname="image", sizes="50vw")
        
        self.assertIn('src="http://nohost/plone/news1/@@images/image', tag)
        self.assertIn('srcset="', tag)
        self.assertIn('sizes="50vw"', tag)

    def test_news_item_tag_brain(self):
        """Test tag method with a News Item brain."""
        brains = api.content.find(id="news1")
        brain = brains[0]
        
        tag = self.helper.tag(brain, fieldname="image", scale="thumb", css_class="thumb-img")
        
        self.assertIn('class="thumb-img"', tag)
        self.assertIn('/@@images/image', tag)
        # Should contain height and width from metadata
        self.assertIn('width="', tag)
        self.assertIn('height="', tag)

    def test_missing_image(self):
        """Test with an item that has no image."""
        self.portal.invokeFactory("News Item", "news2", title="News 2")
        news2 = self.portal.news2
        news2.reindexObject()
        
        brains = api.content.find(id="news2")
        brain = brains[0]
        
        tag = self.helper.srcset(brain, fieldname="image")
        self.assertEqual(tag, "")

    def test_invalid_fieldname(self):
        """Test with an invalid fieldname."""
        brains = api.content.find(id="news1")
        brain = brains[0]
        
        tag = self.helper.srcset(brain, fieldname="nonexistent")
        self.assertEqual(tag, "")

    def test_custom_content_type(self):
        """Test with a custom content type with different image field names."""
        # Programmatically create a simple dexterity type
        from plone.dexterity.fti import DexterityFTI
        from plone.dexterity.content import Item
        from zope.component.factory import Factory

        fti = DexterityFTI("CustomType")
        fti.schema = "cs.srcset.tests.test_helper.ICustomImage"
        fti.klass = "plone.dexterity.content.Item"
        self.portal.portal_types._setOb("CustomType", fti)
        
        # Register FTI as utility
        from zope.component import getSiteManager
        from plone.dexterity.interfaces import IDexterityFTI
        sm = getSiteManager()
        sm.registerUtility(fti, IDexterityFTI, name="CustomType")
        
        # Register factory
        from zope.component.interfaces import IFactory
        from zope.component.factory import Factory
        from plone.dexterity.content import Item
        sm.registerUtility(Factory(Item, title="Custom Type"), IFactory, name="CustomType")

        self.portal.invokeFactory("CustomType", "custom1", title="Custom 1")
        custom1 = self.portal.custom1
        
        image_data = getFile("image.png")
        custom1.photo = NamedImage(image_data, "image/png", "photo.png")
        custom1.logo = NamedImage(image_data, "image/png", "logo.png")
        custom1.reindexObject()
        
        brains = api.content.find(id="custom1")
        brain = brains[0]
        
        # Test photo field
        tag_photo = self.helper.srcset(brain, fieldname="photo", sizes="20vw")
        self.assertIn('srcset="', tag_photo)
        self.assertIn('photo', tag_photo)
        
        # Test logo field
        tag_logo = self.helper.srcset(brain, fieldname="logo", sizes="10vw")
        self.assertIn('srcset="', tag_logo)
        self.assertIn('logo', tag_logo)
