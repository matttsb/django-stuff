from django.conf.urls import url
from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from userprofiles2 import views
from django.conf.urls import include
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'userprofiles', views.UserProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tick/', OnlineView, name='tick-view'),
    path('list/', UserProfileListView.as_view(), name='profile-list-view'),
    path('send/<slug>', SendNew.as_view(), name='send'),
    path('sendmessage/', csrf_exempt(SendMessage.as_view()), name='send-message'),
    path('chatcontents/<slug>', ChatContents.as_view(), name='chatcontents'),
    path('user/<slug>', ProfileDetailView.as_view(), name='user-detail'),
    url(r'^$', ProfileHomeView.as_view(), name='profile-home'),
    url(r'^identity/(?P<pk>[0-9]+)/$',

        ProfileIdentite.as_view(), name='profile-identity-form'),
]
