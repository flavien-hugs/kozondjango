from django.urls import reverse
from django.utils import timezone
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from dashboard.forms import TopicForm, PostForm
from dashboard.models import Dashboard, Topic, Post


# DASHBOARD LISTVIEW
class DashboardListView(ListView):
    model = Dashboard
    template_name = 'dashboard/index.html'


# TOPICS LISTVIEW
class TopicListView(ListView):
    model = Topic
    template_name = 'dashboard/topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['dashboard'] = self.dashboard
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.dashboard = get_object_or_404(Dashboard, pk=self.kwargs.get('pk'))
        queryset = self.dashboard.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


# POST LISTVIEW
class PostListView(ListView):
    model = Post
    template_name = 'dashboard/topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, dashboard__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    dashboard = get_object_or_404(Dashboard, pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.dashboard = dashboard
            topic.user = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('dashboard:topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = TopicForm()

    context = {'dashboard': dashboard, 'form': form}
    template = 'dashboard/new_topic.html'
    return render(request, template, context)


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, dashboard__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('dashboard:topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()

    context = {'topic': topic, 'form': form}
    template = 'dashboard/reply_topic.html'
    return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'dashboard/edit_post.html'
    pk_url_kwarg = 'post_pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        return redirect('dashboard:topic_posts', pk=post.topic.dashboard.pk, topic_pk=post.topic.pk)
