import unittest
from doctest import _ellipsis_match

from cs.srcset.testing import CS_SRCSET_INTEGRATION_TESTING


class TestView(unittest.TestCase):

    layer = CS_SRCSET_INTEGRATION_TESTING

    def testImgSrcSet(self):
        """test rendered srcset values"""
        self.scaling.available_sizes = {
            "huge": (1600, 65536),
            "great": (1200, 65536),
            "larger": (1000, 65536),
            "large": (800, 65536),
            "teaser": (600, 65536),
            "preview": (400, 65536),
            "mini": (200, 65536),
            "thumb": (128, 128),
            "tile": (64, 64),
            "icon": (32, 32),
            "listing": (16, 16),
        }
        tag = self.scaling.srcset("image", sizes="50vw")
        base = self.item.absolute_url()
        expected = f"""<img title="foo" alt="foo" sizes="50vw" srcset="{base}/@@images/image-200-....png 200w, {base}/@@images/image-128-....png 128w, {base}/@@images/image-64-....png 64w, {base}/@@images/image-32-....png 32w, {base}/@@images/image-16-....png 16w" src="{base}/@@images/image-1600-....png".../>"""
        self.assertTrue(_ellipsis_match(expected, tag.strip()))

    def testImgSrcSetCustomSrc(self):
        """test that we can select a custom scale in the src attribute"""
        self.scaling.available_sizes = {
            "huge": (1600, 65536),
            "great": (1200, 65536),
            "larger": (1000, 65536),
            "large": (800, 65536),
            "teaser": (600, 65536),
            "preview": (400, 65536),
            "mini": (200, 65536),
            "thumb": (128, 128),
            "tile": (64, 64),
            "icon": (32, 32),
            "listing": (16, 16),
        }
        tag = self.scaling.srcset("image", sizes="50vw", scale_in_src="mini")
        base = self.item.absolute_url()
        expected = f"""<img title="foo" alt="foo" sizes="50vw" srcset="{base}/@@images/image-200-....png 200w, {base}/@@images/image-128-....png 128w, {base}/@@images/image-64-....png 64w, {base}/@@images/image-32-....png 32w, {base}/@@images/image-16-....png 16w" src="{base}/@@images/image-200-....png".../>"""
        self.assertTrue(_ellipsis_match(expected, tag.strip()))

    def testImgSrcSetInexistentScale(self):
        """test that when requesting an inexistent scale for the src attribute
        we provide the biggest scale we can produce
        """
        self.scaling.available_sizes = {
            "huge": (1600, 65536),
            "great": (1200, 65536),
            "larger": (1000, 65536),
            "large": (800, 65536),
            "teaser": (600, 65536),
            "preview": (400, 65536),
            "mini": (200, 65536),
            "thumb": (128, 128),
            "tile": (64, 64),
            "icon": (32, 32),
            "listing": (16, 16),
        }
        tag = self.scaling.srcset(
            "image", sizes="50vw", scale_in_src="inexistent-scale-name"
        )
        base = self.item.absolute_url()
        expected = f"""<img title="foo" alt="foo" sizes="50vw" srcset="{base}/@@images/image-200-....png 200w, {base}/@@images/image-128-....png 128w, {base}/@@images/image-64-....png 64w, {base}/@@images/image-32-....png 32w, {base}/@@images/image-16-....png 16w" src="{base}/@@images/image-200-....png".../>"""
        self.assertTrue(_ellipsis_match(expected, tag.strip()))

    def testImgSrcSetCustomTitle(self):
        """test passing a custom title to the srcset method"""
        self.scaling.available_sizes = {
            "huge": (1600, 65536),
            "great": (1200, 65536),
            "larger": (1000, 65536),
            "large": (800, 65536),
            "teaser": (600, 65536),
            "preview": (400, 65536),
            "mini": (200, 65536),
            "thumb": (128, 128),
            "tile": (64, 64),
            "icon": (32, 32),
            "listing": (16, 16),
        }
        tag = self.scaling.srcset("image", sizes="50vw", title="My Custom Title")
        base = self.item.absolute_url()
        expected = f"""<img title="My Custom Title" alt="foo" sizes="50vw" srcset="{base}/@@images/image-200-....png 200w, {base}/@@images/image-128-....png 128w, {base}/@@images/image-64-....png 64w, {base}/@@images/image-32-....png 32w, {base}/@@images/image-16-....png 16w" src="{base}/@@images/image-1600-....png".../>"""
        self.assertTrue(_ellipsis_match(expected, tag.strip()))

    def testImgSrcSetAdditionalAttributes(self):
        """test that additional parameters are output as is, like alt, loading, ..."""
        self.scaling.available_sizes = {
            "huge": (1600, 65536),
            "great": (1200, 65536),
            "larger": (1000, 65536),
            "large": (800, 65536),
            "teaser": (600, 65536),
            "preview": (400, 65536),
            "mini": (200, 65536),
            "thumb": (128, 128),
            "tile": (64, 64),
            "icon": (32, 32),
            "listing": (16, 16),
        }
        tag = self.scaling.srcset(
            "image",
            sizes="50vw",
            alt="This image shows nothing",
            css_class="my-personal-class",
            title="My Custom Title",
            loading="lazy",
        )
        base = self.item.absolute_url()

        expected = f"""<img title="My Custom Title" alt="This image shows nothing" class="my-personal-class" loading="lazy" sizes="50vw" srcset="{base}/@@images/image-200-....png 200w, {base}/@@images/image-128-....png 128w, {base}/@@images/image-64-....png 64w, {base}/@@images/image-32-....png 32w, {base}/@@images/image-16-....png 16w" src="{base}/@@images/image-1600-....png".../>"""
        self.assertTrue(_ellipsis_match(expected, tag.strip()))
