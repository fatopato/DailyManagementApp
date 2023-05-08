from django.urls import path
from .views import login_view, create_user, no_team_member
from .views import (
    OrganizationListView,
    OrganizationCreateView,
    OrganizationUpdateView,
    OrganizationDeleteView,
    TeamListView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    DailyListView,
    DailyCreateView,
    DailyUpdateView,
    DailyDeleteView,
    DailyItemCreateView,
    DailyItemUpdateView,
    DailyItemDeleteView,
    CustomLoginView,
    DailyItemList
)

app_name = 'core'  # define the app namespace

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # Organizations
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organizations/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organizations/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),

    # Teams
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/create/', TeamCreateView.as_view(), name='team-create'),
    path('teams/<int:pk>/update/', TeamUpdateView.as_view(), name='team-update'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team-delete'),

    # Daily
    path('daily/', DailyListView.as_view(), name='daily-list'),
    path('daily/create/', DailyCreateView.as_view(), name='daily-create'),
    path('daily/<int:pk>/update/', DailyUpdateView.as_view(), name='daily-update'),
    path('daily/<int:pk>/delete/', DailyDeleteView.as_view(), name='daily-delete'),

    # DailyItem
    path('dailyitem/create/', DailyItemCreateView.as_view(), name='dailyitem-create'),
    path('dailyitem/<int:pk>/update/', DailyItemUpdateView.as_view(), name='dailyitem-update'),
    path('dailyitem/<int:pk>/delete/', DailyItemDeleteView.as_view(), name='dailyitem-delete'),
    path('dailyitem_list/', DailyItemList.as_view(), name='dailyitem_list'),

    path('create-user/', create_user, name='create-user'),
    path('no_team_member/', no_team_member, name='no_team_member'),

]
