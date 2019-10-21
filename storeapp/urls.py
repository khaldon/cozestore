from django.urls import path
from . import views

app_name = 'storeapp'

urlpatterns = [
    path('post/', views.PostListView.as_view(), name='post_list'), 
    path('post/tag/<tag_slug>', views.PostListView.as_view(), name='post_list_by_tag'), 
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]