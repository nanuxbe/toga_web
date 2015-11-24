from django.conf.urls import include, url
from django.contrib import admin

from rest_framework_nested import routers

from sample.api import (ProfileViewSet, PopularUserCookBookViewSet, LatestUserCookBookViewSet,
    UserRecipesViewSet)
from sample.views import UsersListView


router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet, base_name='users')
user_router = routers.NestedSimpleRouter(router, r'profiles', lookup='user')
user_router.register(r'latest_cookbooks', LatestUserCookBookViewSet, base_name='user-latest_cookbooks')
user_router.register(r'popular_cookbooks', PopularUserCookBookViewSet, base_name='user-popular_cookbooks')
user_router.register(r'recipes', UserRecipesViewSet, base_name='user-recipes')

urlpatterns = [
    # Examples:
    # url(r'^$', 'toga_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', UsersListView.as_view(), name='home'),

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(user_router.urls))
]
