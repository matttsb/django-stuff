from django.shortcuts import render
from django.views import generic
from heating import *
from heating.models import Appliance, Manufacturer, Part, BlogPost, BlogCategory
from django.contrib.auth import logout
from django.shortcuts import redirect
from userprofiles2.models import UserProfile
from django_comments.models import Comment



def index(request):
    return render(request, 'index.html')


class PostDetail(generic.DetailView):
    # no need to change this can render in blog detail template
    model = BlogPost
    template_name = 'post_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        return context

class ForumDetail(generic.DetailView):
    # no need to change this can render in blog detail template
    model = BlogPost
    template_name = 'forum_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ForumDetail, self).get_context_data(**kwargs)
        return context

class IndexView(generic.TemplateView):
    template_name = 'overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_appliances'] = Appliance.objects.all().filter(visible=True)[:5]
        #context['latest_parts']= Part.objects.order_by("mpn")[:10]
        context['latest_news'] = BlogPost.objects.all().filter(category=2,visible=True)[:5]
        context['latest_secret_plumber'] = BlogPost.objects.all().filter(category=1,visible=True)[
            :5]
        context['latest_features'] = BlogPost.objects.all().filter(category=4,visible=True)[
            :5]
        context['latest_reviews'] = BlogPost.objects.all().filter(category=3,visible=True)[
            :5]
        context['online_users'] = UserProfile.objects.all()[:5]
        context['events'] = BlogPost.objects.all().filter(category=6,visible=True)[:5]
        return context

class FrontPageView(generic.TemplateView):
    template_name = 'frontpageview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_features'] = BlogPost.objects.all().filter(visible=True)[
            :40].select_related('category')
        context['ctx'] = context['latest_features']
        return context

def redirect_view(request):
    response = redirect('/redirect-success/')
    return response


def logout_view(request):
    logout(request)
    response = redirect('/manage/')
    return response


class ApplianceListView(generic.ListView):
    model = Appliance
    paginate_by = 10


class PartListView(generic.ListView):
    context_object_name = 'part_list'
    model = Part


class ApplianceDetailView(generic.DetailView):
    model = Appliance


def manage(request):
    return render(request, 'manage.html')


class SinglePostByCategory(generic.DetailView):
    model = BlogPost

    def get_queryset(self):
        return get_object_or_404(Post,
                                 category_slug=self.kwargs['category_slug'],
                                 slug=self.kwargs['post_slug']
                                 )
