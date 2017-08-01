from django.conf.urls import url
from . import views

app_name="client"

urlpatterns = [
    #url(r'^show/(?P<pk>\d+)$', views.ShowView.as_view(),name ="show"),
    url(r'^show/(?P<username_url>\w+)$', views.ShowClass.as_view(),name ="show"),
    url(r'^login/$', views.LoginClass.as_view(),name="login"),
    url(r'^logout/$', views.logout,name="logout"),
    url(r'^dashboard/$', views.DashboardClass.as_view(),name="dashboard"),
    url(r'^create/$', views.CreateClass.as_view(),name="create"),
    url(r'^edit/$', views.EditClass.as_view(),name="edit"),
    url(r'^edit_password/$', views.edit_password,name="edit_password"),
]