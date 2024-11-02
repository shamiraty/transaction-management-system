
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('app.urls')),  # Include your app's URLs
         path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

from django.contrib import admin

admin.site.site_header = "ADMINISTRATION"
admin.site.index_title = "ADMINISTRATION"
admin.site.site_title = "ADMINISTRATION"

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
   