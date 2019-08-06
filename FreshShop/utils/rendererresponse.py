from rest_framework.renderers import JSONRenderer


class CustomerRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = data.pop("msg","没有这个字段")
                code = data.pop("code", 0)
            else:
                msg = "没有这个字段"
                code = 0
            result = {
                "msg":msg,
                "code":code,
                "data":data
            }
            return super().render(result, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)