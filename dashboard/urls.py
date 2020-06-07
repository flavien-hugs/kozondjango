from django.urls import path

from dashboard.views import TopicListView, new_topic, PostListView, reply_topic, PostUpdateView

app_name = 'dashboard'
urlpatterns = [
    path('topics/<pk>', TopicListView.as_view(), name='topics_dashboard'),
    path('<pk>/new/', new_topic, name='new_topic'),
    path('<pk>/topics/<topic_pk>/', PostListView.as_view(), name='topic_posts'),
    path('<pk>/topics/<topic_pk>/reply/', reply_topic, name='reply_topic'),
    path('<pk>/topics/<topic_pk>/posts/<post_pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
]
