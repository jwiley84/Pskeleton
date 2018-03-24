from django.conf.urls import url
from . import views #(imports views.py of the current folder)

urlpatterns = [ 
    url(r'^$', views.index), 
    url(r'^register', views.register),
    url(r'login', views.login),
    url(r'success', views.success),
    url(r'^rev_create', views.rev_create), # POST data from ADD to the DB
    url(r'^user/(?P<id>\d+)', views.uShow), #display the particular book 
    url(r'^fav_btn', views.fav_btn),
    url(r'^unfav_btn', views.unfav_btn),
    url(r'logout', views.logout)
    ]