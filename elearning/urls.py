from django.conf.urls import url
from elearning import views

urlpatterns = [
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^register$',views.register),
    url(r'^tree$',views.tree),
    url(r'^homework_answer/(?P<node_id>\w+)$',views.get_homework_answer),
    url(r'^homework_answer$',views.set_homework_answer),
    url(r'^homework$',views.set_homework),
    url(r'^homework/(?P<node_id>\w+)$',views.get_homework),
    url(r'^downloadfile/(?P<material_id>\w+)$',views.download_material),
    # url(r'^uploadfile/(?P<material_id>\w+)$',views.upload_material),
    url(r'^materials/(?P<node_id>\w+)$',views.get_materials),
    url(r'^materials$',views.create_material),
]