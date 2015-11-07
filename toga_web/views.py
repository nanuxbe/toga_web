from django.views import TemplateView


class ComponentOptions(object):
    endpoint = None
    serializer_class = None
    verb = 'GET'
    target = None


class BaseComponent(object):
    pass


class Component(BaseComponent):
    pass


class ComponentList:
    pass


class PageView(ComponentList, TemplateView):
    pass

