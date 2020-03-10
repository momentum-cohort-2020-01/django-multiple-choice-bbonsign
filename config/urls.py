from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from snippets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('', views.user_home, name='user_home'),
    path('snippet/<int:snip_id>', views.snippet_detail, name='snippet_detail'),
    path('add-snippet', views.add_snippet, name='add_snippet'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
