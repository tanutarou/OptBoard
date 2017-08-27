from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.project_select, name='project_select'),
    url(r'^project/add$', views.project_edit, name='project_add'),
    url(r'^project/edit/(?P<edit_project_id>\d+)$', views.project_edit, name='project_edit'),
    url(r'^project/del/(?P<del_project_id>\d+)$', views.project_del, name='project_del'),
    url(r'^(?P<project_id>\d+)/$', views.main_page, name='main'),
    url(r'^(?P<project_id>\d+)/result/del/(?P<del_result_id>\d+)/$', views.result_del, name='result_del'),
    url(r'^(?P<project_id>\d+)/result/del/all/$', views.result_del_all, name='result_del_all'),
    url(r'^(?P<project_id>\d+)/solver/$', views.solver_list, name='solver_list'),
    url(r'^(?P<project_id>\d+)/solver/add$', views.solver_edit, name='solver_add'),
    url(r'^(?P<project_id>\d+)/solver/edit/(?P<solver_id>\d+)/$', views.solver_edit, name='solver_edit'),
    url(r'^(?P<project_id>\d+)/solver/del/(?P<solver_id>\d+)/$', views.solver_del, name='solver_del'),
    url(r'^(?P<project_id>\d+)/analysis/1D$', views.analysis1D, name='analysis1D'),
    url(r'^(?P<project_id>\d+)/analysis/2D$', views.analysis2D, name='analysis2D'),
]
