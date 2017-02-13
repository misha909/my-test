from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.user_list, name='index'),
    url(r'^add/$', views.add_user, name='add'),
    url(r'^edit/(?P<user_id>\d+)/$', views.edit_user, name='edit'),
    url(r'^delete/(?P<user_id>\d+)/$', views.delete_user, name='delete'),
    url(r'^download/$', views.download, name='download'),
]