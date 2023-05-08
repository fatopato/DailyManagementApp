from django.contrib import admin
from .models import TeamMember, Organization, Team, Daily, DailyItem

admin.site.register(TeamMember)
admin.site.register(Organization)
admin.site.register(Team)
admin.site.register(Daily)
admin.site.register(DailyItem)