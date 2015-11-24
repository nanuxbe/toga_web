from django.views import TemplateView
from .components.dummy import ComponentList


class PageView(ComponentList, TemplateView):
    pass

