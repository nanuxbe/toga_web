from .views import Component

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin


class DetailComponent(SingleObjectMixin, Component):
    pass


class ListComponent(MultipleObjectMixin, Component):
    pass

