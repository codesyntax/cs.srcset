from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


class IImageHelper(Interface):
    """Marker interface for ImageHelper"""


@implementer(IImageHelper)
class ImageHelper(BrowserView):
    def srcset(self, item, fieldname="image", **kwargs):
        """Generate srcset img tag from brain metadata or fallback to getObject()."""
        return self._render("srcset", item, fieldname, **kwargs)

    def tag(self, item, fieldname="image", **kwargs):
        """Generate fixed img tag from brain metadata or fallback to getObject()."""
        return self._render("tag", item, fieldname, **kwargs)

    def _render(self, method_name, item, fieldname, **kwargs):
        # Try to use metadata if available
        if hasattr(item, "image_scales"):
            image_scales = getattr(item, "image_scales", None)
            if image_scales and fieldname in image_scales:
                field_data = image_scales[fieldname]
                if isinstance(field_data, list) and len(field_data) > 0:
                    data = field_data[0]
                    if method_name == "srcset":
                        return self._generate_srcset_tag(item, data, **kwargs)
                    else:
                        return self._generate_fixed_tag(item, data, **kwargs)

        # Eager Fallback
        obj = item.getObject() if hasattr(item, "getObject") else item
        try:
            scales = obj.restrictedTraverse("@@images")
            if hasattr(scales, method_name):
                method = getattr(scales, method_name)
                res = method(fieldname, **kwargs)
                return res if res is not None else ""

            # If @@images doesn't have it, try our own backport view
            if method_name == "srcset":
                backport = obj.restrictedTraverse("@@images-srcset")
                return backport.srcset(fieldname, **kwargs)
        except Exception:
            return ""

    def _generate_srcset_tag(self, item, data, **kwargs):
        """Manually construct the srcset <img> tag from brain metadata."""
        base_url = item.getURL() if hasattr(item, "getURL") else item.absolute_url()
        if callable(base_url):
            base_url = base_url()

        scales = data.get("scales", {})
        src_url = f"{base_url}/{data['download']}"

        srcset_parts = []
        sorted_scales = sorted(scales.items(), key=lambda x: x[1].get("width", 0))
        for _, scale_info in sorted_scales:
            scale_url = f"{base_url}/{scale_info['download']}"
            width = scale_info.get("width")
            if width:
                srcset_parts.append(f"{scale_url} {width}w")

        srcset = ", ".join(srcset_parts)

        alt = kwargs.get("alt")
        if alt is None:
            alt = getattr(item, "Title", "")
            if callable(alt):
                alt = alt()

        return self._build_tag(
            src_url,
            srcset=srcset,
            width=data.get("width"),
            height=data.get("height"),
            alt=alt,
            **kwargs,
        )

    def _generate_fixed_tag(self, item, data, **kwargs):
        """Manually construct a fixed <img> tag from brain metadata."""
        base_url = item.getURL() if hasattr(item, "getURL") else item.absolute_url()
        if callable(base_url):
            base_url = base_url()

        scales = data.get("scales", {})

        # If a specific scale is requested via scale parameter
        scale_name = kwargs.get("scale")
        if scale_name and scale_name in scales:
            scale_info = scales[scale_name]
            src_url = f"{base_url}/{scale_info['download']}"
            width = scale_info.get("width")
            height = scale_info.get("height")
        else:
            # Fallback to original
            src_url = f"{base_url}/{data['download']}"
            width = data.get("width")
            height = data.get("height")

        # Override width/height if passed in kwargs (for tag method)
        width = kwargs.get("width", width)
        height = kwargs.get("height", height)

        alt = kwargs.get("alt")
        if alt is None:
            alt = getattr(item, "Title", "")
            if callable(alt):
                alt = alt()

        return self._build_tag(
            src_url,
            width=width,
            height=height,
            alt=alt,
            **kwargs,
        )

    def _build_tag(self, src, srcset=None, **kwargs):
        """Helper to build the <img> tag string."""
        tag = f'<img src="{src}"'
        if srcset:
            tag += f' srcset="{srcset}"'

        # Possible attributes from kwargs
        attrs = ("sizes", "alt", "title", "loading", "width", "height")
        for attr in attrs:
            val = kwargs.get(attr)
            if val:
                tag += f' {attr}="{val}"'
            elif attr == "loading" and "loading" not in kwargs:
                tag += ' loading="lazy"'

        css_class = kwargs.get("css_class") or kwargs.get("class")
        if css_class:
            tag += f' class="{css_class}"'

        tag += " />"
        return tag
