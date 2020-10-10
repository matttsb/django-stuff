from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofiles2.models import UserProfile, Chat
from userprofiles2.forms import IdentiteForm
from django.views import generic
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import pytz
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from userprofiles2.serializers import *
from django.views.generic.base import RedirectView
from django.shortcuts import redirect

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-last_seen')
    serializer_class = UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserProfileListView(generic.ListView):
    template_name = 'userprofiles2/user_list.html'
    model = User
    paginate_by = 12


class ProfileHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofiles2/home.html'
    user_check_failure_path = reverse_lazy("account_signup")

    def check_user(self, user):
        if user.is_active:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        context['profile'] = profile
        return context


class ProfileIdentite(LoginRequiredMixin, UpdateView):
    template_name = "userprofiles2/identity_form.html"
    form_class = IdentiteForm
    user_check_failure_path = reverse_lazy("account_signup")
    success_url = reverse_lazy("profile-home")

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset

    def form_valid(self, form, **kwargs):
        super(ProfileIdentite, self).form_valid(form)
        profile = form.save(commit=False)
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        profile.gender = form.cleaned_data['gender']
        profile.phone = form.cleaned_data['phone']
        profile.personal_info_is_completed = True
        profile.completion_level = profile.get_completion_level()
        profile.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileDetailView(DetailView):
    template_name = "userprofiles2/profile.html"
    model = User

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('slug'))


def OnlineView(request):
    if request.user.is_authenticated:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.last_seen = timezone.now()
        userprofile.save()
    return HttpResponse(request.user.id)


class ChatContents(TemplateView):
    template_name = 'userprofiles2/chatcontents.html'

    def get(self, request, **kwargs):
        sender = None
        if request.user.is_authenticated:
            username = request.user.username
            sender = User.objects.get(username=username)
        try:
            receiver = User.objects.get(username=self.kwargs.get('slug'))
        except BaseException:
            receiver = User.objects.get(pk=self.kwargs.get('slug'))
        context = {}
        context['chat'] = Chat.objects.all().filter(Q(receiver=receiver) | Q(
            sender=receiver), owner=sender).order_by('date')[:100]
        context['receiverid'] = receiver.pk
        return super(TemplateView, self).render_to_response(context)


def buildcontext(user, sender, receiver, rid):
    context = {}
    context['chat'] = Chat.objects.all().filter(Q(receiver=receiver) | Q(
        sender=receiver), owner=user).order_by('date')[:100]
    context['users'] = Chat.objects.only('otherparty').values(
        'otherparty').distinct().filter(owner=sender)[:26]
    context['receiverid'] = rid
    return context


class SendMessage(TemplateView):
    template_name = 'userprofiles2/chat.html'

    def post(self, request, **kwargs):
        data = request.POST
        if request.user.is_authenticated:
            sender = request.user
            receiver = User.objects.get(pk=data['receiver'])
            if data['message']:
                c = Chat.objects.create(
                    owner=sender,
                    otherparty=receiver,
                    sender=sender,
                    receiver=receiver,
                    body=data['message'],
                    type='T',
                    status='U')
                c = Chat.objects.create(
                    owner=receiver,
                    otherparty=sender,
                    sender=sender,
                    receiver=receiver,
                    body=data['message'],
                    type='T',
                    status='U')
                return super(
                    TemplateView,
                    self).render_to_response(
                    buildcontext(
                        sender,
                        sender,
                        receiver,
                        data['receiver']))
        else:
            response = redirect(reverse_lazy('account_login',))
            return response          


class SendNew(TemplateView):
    template_name = 'userprofiles2/chat.html'

    def get(self, request, **kwargs):
        sender = None
        if request.user.is_authenticated:
            username = request.user.username
            sender = request.user
            receiver = User.objects.get(username=self.kwargs.get('slug'))
            return super(
                TemplateView,
                self).render_to_response(
                buildcontext(
                    sender,
                    sender,
                    receiver,
                    receiver.pk))
        else:
            response = redirect(reverse_lazy('account_login',))
            return response