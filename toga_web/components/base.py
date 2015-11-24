from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured
from django.utils import six


class ComponentOptions(object):

    def __init__(self, options=None):
        self.endpoint = getattr(options, 'endpoint', None)
        self.serializer_class = getattr(options, 'serializer_class', None)
        self.verb = getattr(options, 'verb', 'GET')
        self.target = getattr(options, 'target', None)


class ComponentMetaClass(type):
    
    def __new__(cls, name, bases, attrs, meta_class=ComponentOptions):
        new_class = super(ComponentMetaClass, cls).__new__(cls, name, bases, attrs)

        if bases == (BaseComponent, ):
            return new_class

        opts = new_class._meta = meta_class(getattr(new_class, 'Meta', None))

        if opts.serializer_class is None:
            raise ImproperlyConfigured('A component needs to define an endpoint')

        return new_class


class BaseComponent(object):
    
    def render(self, request):
        raise NotImplementedError('Please implement a proper render method')


class DeclarativeComponentsMetaClass(ComponentMetaClass):
    """
    Metaclass that collects Components declared on the base classes.
    """

    def __new__(cls, name, bases, attrs):
        # Locally declared components
        components_list = []
        for key, value in list(attrs.items()):
            if isinstance(value, BaseComponent):
                components_list.append((key, value))
                attrs.pop(key)
        attrs['declared_components'] = OrderedDict(components_list)

        new_class = super(DeclarativeComponentsMetaClass, cls)).__new__(
                cls, name, bases, attrs
        )

        # Ancestors-declared components
        declared_components = OrderedDict()
        for base in reversed(new_class.__mro__):
            if hasattr(base, 'declared_components'):
                declared_components.update(base.declared_components)

            # Ability to "undeclare" parent-declared component
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_components:
                    declared_components.pop(attr)

        new_class.declared_components = declared_components

        return new_class


class ComponentMixin(six.with_metaclass(ComponentMetaClass, BaseComponent)):

    def __init__(self):
        opts = self._meta

        if opts.serializer_class is None:
            raise ImproperlyConfigured('Leaf component has no serializer_class specified')

    @property
    def _base_fields:
        return self._meta.serializer_class().fields


class ComponentListMixin(six.with_metaclass(DeclarativeComponentsMetaClass, BaseComponent)):

    @property
    def component_names:
        return self.declared_components.keys()

    def get_context_data(self, **kwargs):
        context = super(ComponentListMixin, self).get_context_data(**kwargs)

        components = {}

        for key, component in self.declared_components.items():
            components[key] = component.render(request)

        context['components'] = components
        context['component_names'] = self.component_names

        return context
