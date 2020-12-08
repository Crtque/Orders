from django.urls import path
from . import Views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', Views.home, name='home'),
    path('auth/', Views.auth, name='auth'),
    path('exit/', Views.exit, name='exit'),
    path('manage/', Views.manage, name='manage'),
    path('manageorg/', Views.manageorg, name="manageorg"),
    path('taskoforg/', Views.taskoforg, name="taskoforg"),
    path('usersadm/',Views.usersadm,name="usersadm")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)