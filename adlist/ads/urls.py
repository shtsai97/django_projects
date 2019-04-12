from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.AdListView.as_view()),
    path('ads', views.AdListView.as_view(), name='ads'),
    path('ads/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/create',
        views.AdFormView.as_view(success_url=reverse_lazy('ads')), name='ad_create'),
    path('ads/<int:pk>/update',
        views.AdFormView.as_view(success_url=reverse_lazy('ads')), name='ad_update'),
    path('ads/<int:pk>/delete',
        views.AdDeleteView.as_view(success_url=reverse_lazy('ads')), name='ad_delete'),
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
    path('ads/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='comment_delete'),
    path('ads/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='ad_favorite'),
    path('ads/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='ad_unfavorite'),
]
