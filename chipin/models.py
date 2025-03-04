from django.db import models
from django.contrib.auth.models import User

from users.models import CustomUser


class Group(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(
        CustomUser, related_name="admin_groups", on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        CustomUser, related_name="group_memberships", blank=True
    )
    invited_users = models.ManyToManyField(
        CustomUser, related_name="pending_invitations", blank=True
    )

    def __str__(self):
        return self.name


class GroupJoinRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="join_requests"
    )
    is_approved = models.BooleanField(default=False)
    votes = models.ManyToManyField(
        CustomUser, related_name="votes", blank=True
    )  # Tracks users who voted
    created_at = models.DateTimeField(auto_now_add=True)
