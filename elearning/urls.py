from django.conf.urls import url
from elearning import views

urlpatterns = [
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^register$',views.register),
    url(r'^tree$',views.tree),
    # url(r'^node/(?P<node_id>\w+)/homework_answer$',views.get_homework_answer),
    # url(r'^node/(?P<node_id>\w+)/homework_answer$',views.set_homework_answer),
    url(r'^node/(?P<node_id>\w+)/homework$',views.HomeworkView.as_view()),
    url(r'^node/(?P<node_id>\w+)/homeworkanswer$',views.HomeworkAnswerView.as_view()),
    # url(r'^node/(?P<node_id>\w+)/homework$',views.set_homework),
    # url(r'^node/(?P<node_id>\w+)/homework$',views.get_homework),
    # url(r'^downloadfile/(?P<material_id>\w+)$',views.download_material),
    # url(r'^uploadfile/(?P<material_id>\w+)$',views.FileUploadView.as_view()),
    # url(r'^material/(?P<material_id>\w+)$',views.MaterialFileView.as_view()),
    url(r'^node/(?P<node_id>\w+)/materials$',views.get_materials),
    # url(r'^materials$',views.create_material),
    url(r'^node/(?P<node_id>\w+)/material$',views.MaterialFileUploadView.as_view()),
    url(r'^node/(?P<node_id>\w+)/material/(?P<material_id>\w+)$',views.MaterialFileDownloadView.as_view()),
]