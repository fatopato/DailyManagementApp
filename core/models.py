from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Organization(models.Model):
    title = models.CharField(unique=True, null=True, blank=True, max_length=100)

    def __str__(self):
        return self.title if self.title else str(self.pk)


class Team(models.Model):
    title = models.CharField(unique=True, null=True, blank=True, max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.title if self.title else str(self.pk)


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Daily(models.Model):
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.title + "-" + str(self.date)


class DailyItem(models.Model):
    STATUS_CHOICES = [
        ('NS', 'Not Started'),
        ('BL', 'Blocked'),
        ('IP', 'In Progress'),
        ('CM', 'Completed'),
    ]
    title = models.CharField(unique=True, null=True, blank=True, max_length=100)
    daily = models.ForeignKey(Daily, on_delete=models.CASCADE)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NS')
    progress_note = models.TextField(blank=True)

    class Meta:
        unique_together = ('daily', 'team_member', 'description')

    def __str__(self):
        return self.title if self.title else str(self.pk)
