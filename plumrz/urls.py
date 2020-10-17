from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from heating import views
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import logout
from allauth import urls
from avatar import urls
from django.views.generic.base import TemplateView

urlpatterns = [
    path('',views.FrontPageView.as_view()),
    path('comments/', include('django_comments.urls')),
    path('comment/', include('comment.urls')),
    path('questions/<slug:slug>/', views.ForumDetail.as_view(), name='forum-detail'),
    path('<slug:category>/<slug:slug>/', views.PostDetail.as_view(), name='blogpost-detail'),
    path('overview/',views.IndexView.as_view()),
    path('manage/', views.manage, name='manage'),
    path('api/', include('comment.api.urls')),  # for API Framework
    path('avatar/', include('avatar.urls')),
    path('account/', include('allauth.urls')),
    path('profile/', include('userprofiles2.urls')),
    path('newsfeed/', include('newsfeed.urls', namespace='newsfeed')),
    path('accounts/profile/',  TemplateView.as_view(template_name='profile.html')),
    path('appliance/<slug>/', views.ApplianceDetailView.as_view(), name='appliance-detail'),  
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('appliances/', views.ApplianceListView.as_view(), name='appliances'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
