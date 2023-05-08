from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import ListView

from .models import Daily, DailyItem, Organization, Team, TeamMember


def login_view(request):
    form = AuthenticationForm(request=request)
    return render(request, 'registration/login.html', {'form': form})


class OrganizationListView(ListView):
    model = Organization


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name']
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name']
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    success_url = reverse_lazy('organization-list')


class TeamListView(ListView):
    model = Team


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['name', 'organization']
    success_url = reverse_lazy('team-list')


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    fields = ['name', 'organization']
    success_url = reverse_lazy('team-list')


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('team-list')


class DailyListView(ListView):
    model = Daily


class DailyCreateView(LoginRequiredMixin, CreateView):
    model = Daily
    fields = ['date', 'team']
    success_url = reverse_lazy('daily-list')


class DailyUpdateView(LoginRequiredMixin, UpdateView):
    model = Daily
    fields = ['date', 'team']
    success_url = reverse_lazy('daily-list')


class DailyDeleteView(LoginRequiredMixin, DeleteView):
    model = Daily
    success_url = reverse_lazy('daily-list')


class DailyItemCreateView(LoginRequiredMixin, CreateView):
    model = DailyItem
    fields = ['daily', 'team_member', 'description', 'status', 'progress_note']
    success_url = reverse_lazy('daily-list')

    def form_valid(self, form):
        # Set the user field to the currently logged-in user
        form.instance.team_member = self.request.user
        return super().form_valid(form)


class DailyItemUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyItem
    fields = ['daily', 'team_member', 'description', 'status', 'progress_note']
    success_url = reverse_lazy('daily-list')


class DailyItemDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyItem
    success_url = reverse_lazy('daily-list')


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create the new user object and save it
            user = form.save()
            # Add the user to any selected teams
            selected_teams = request.POST.getlist('teams')
            for team_id in selected_teams:
                team = Team.objects.get(id=team_id)
                user.teams.add(team)
            # Redirect the user to a success page or team selection page
            return redirect('team-select')
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form, 'teams': Team.objects.all()})


def no_team_member(request):
    raise Http404("You don't have a Team Member object")


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        try:
            team_member = TeamMember.objects.get(username=user.username)
        except TeamMember.DoesNotExist:
            return reverse_lazy('core:no_team_member')

        if team_member.teams.count() > 1:
            return reverse_lazy('core:organization_list')
        elif team_member.teams.count() == 1:
            return reverse_lazy('core:team_daily_list', kwargs={'team_id': team_member.teams.first().id})


class DailyItemList(ListView):
    model = DailyItem
    template_name = 'dailyitem_list.html'
    context_object_name = 'dailyitems'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by teamMember
        team_member_id = self.request.GET.get('team_member_id')
        if team_member_id:
            queryset = queryset.filter(team_member_id=team_member_id)

        # Filter by date
        date_str = self.request.GET.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(daily__date=date)
        else:
            # By default, show DailyItems for the current date
            today = timezone.now().date()
            queryset = queryset.filter(daily__date=today)

        return queryset
