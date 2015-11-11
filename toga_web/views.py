from django.views import TemplateView
from .components import ComponentList


class PageView(ComponentList, TemplateView):
    pass

