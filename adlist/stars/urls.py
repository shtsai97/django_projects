from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.StarListView.as_view()),
    path('stars', views.StarListView.as_view(), name='stars'),
    path('stars/<int:pk>', views.StarDetailView.as_view(), name='star_detail'),
    path('stars/create',
        views.StarFormView.as_view(success_url=reverse_lazy('stars')), name='star_create'),
    path('stars/<int:pk>/update',
        views.StarFormView.as_view(success_url=reverse_lazy('stars')), name='star_update'),
    path('stars/<int:pk>/delete',
        views.StarDeleteView.as_view(success_url=reverse_lazy('stars')), name='star_delete'),
    path('stars_picture/<int:pk>', views.stream_file, name='star_picture'),
    path('stars/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('stars')), name='comment_delete'),
]
