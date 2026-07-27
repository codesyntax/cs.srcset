from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


class IImageHelper(Interface):
    """Marker interface for ImageHelper"""


@implementer(IImageHelper)
class ImageHelper(BrowserView):
    def srcset(self, item, fieldname="image", scale_in_src="huge", **kwargs):
        """Generate srcset img tag from brain metadata or fallback to getObject()."""
        kwargs["scale_in_src"] = scale_in_src
        return self._render("srcset", item, fieldname, **kwargs)

    def tag(self, item, fieldname="image", scale=None, **kwargs):
        """Generate fixed img tag from brain metadata or fallback to getObject()."""
        kwargs["scale"] = scale
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
                # Remove internal helper params before passing to @@images
                call_kwargs = kwargs.copy()
                call_kwargs.pop("scale_in_src", None)
                res = method(fieldname, **call_kwargs)
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

        # Determine src scale
        scale_in_src = kwargs.pop("scale_in_src", "huge")
        if scale_in_src in scales:
            scale_info = scales[scale_in_src]
            src_url = f"{base_url}/{scale_info['download']}"
            width = scale_info.get("width")
            height = scale_info.get("height")
        else:
            src_url = f"{base_url}/{data['download']}"
            width = data.get("width")
            height = data.get("height")

        srcset_parts = []
        sorted_scales = sorted(scales.items(), key=lambda x: x[1].get("width", 0))
        for _, scale_info in sorted_scales:
            scale_url = f"{base_url}/{scale_info['download']}"
            swidth = scale_info.get("width")
            if swidth:
                srcset_parts.append(f"{scale_url} {swidth}w")

        srcset = ", ".join(srcset_parts)

        # Merge parameters
        merged = kwargs.copy()
        if "width" not in merged:
            merged["width"] = width
        if "height" not in merged:
            merged["height"] = height

        return self._build_tag(src_url, srcset=srcset, **merged)

    def _generate_fixed_tag(self, item, data, **kwargs):
        """Manually construct a fixed <img> tag from brain metadata."""
        base_url = item.getURL() if hasattr(item, "getURL") else item.absolute_url()
        if callable(base_url):
            base_url = base_url()

        scales = data.get("scales", {})

        # If a specific scale is requested via scale parameter
        scale_name = kwargs.pop("scale", None)
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

        # Merge parameters
        merged = kwargs.copy()
        if "width" not in merged:
            merged["width"] = width
        if "height" not in merged:
            merged["height"] = height

        return self._build_tag(src_url, **merged)

    def _build_tag(self, src, srcset=None, **kwargs):
        """Helper to build the <img> tag string."""
        tag = f'<img src="{src}"'
        if srcset:
            tag += f' srcset="{srcset}"'

        # Handle class/css_class
        css_class = kwargs.pop("css_class", None) or kwargs.pop("class", None)
        if css_class:
            tag += f' class="{css_class}"'

        # Render remaining attributes
        for attr, val in sorted(kwargs.items()):
            if val is not None:
                tag += f' {attr}="{val}"'

        tag += " />"
        return tag
