from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model

from .models import CookBook, Recipe
from .serializers import UserSerializer, CookBookSerializer, RecipeSerializer


class SmallResultsSetPagination(PageNumberPagination):

    page_size = 7


class MediumResultsSetPagination(PageNumberPagination):

    page_size = 15


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class NestedViewSetMixin(object):

    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        qs = super(NestedViewSetMixin, self).get_queryset()
        return qs.filter(user=self.request.parser_context['kwargs']['user_pk'])


class LatestUserCookBookViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):

    queryset = CookBook.objects.order_by('-created')
    serializer_class = CookBookSerializer


class PopularUserCookBookViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):

    queryset = CookBook.objects.order_by('-likes')
    serializer_class = CookBookSerializer


class UserRecipesViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Recipe.objects.order_by('-likes')
    serializer_class = RecipeSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):
        qs = super(UserRecipesViewSet, self).get_queryset()
        return qs.filter(cookbook__user=self.request.parser_context['kwargs']['user_pk'])
