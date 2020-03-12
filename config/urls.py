from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from snippets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('', views.user_home, name='user_home'),
    path('snippet/<int:snip_id>', views.snippet_detail, name='snippet_detail'),
    path('fork/<int:snip_id>', views.fork, name='fork'),
    path('add-snippet/', views.add_snippet, name='add_snippet'),
    path('all-public/', views.all_public, name='all_public'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
