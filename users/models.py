from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet

# from chipin.models import Group

# Generate a key for encryption (store this securely, such as in environment variables)
key = Fernet.generate_key()
cipher_suite = Fernet(key)


class CustomUser(AbstractUser):
    # We will only store essential data: email and nickname
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_profile_public = models.BooleanField(
        default=False
    )  # User controls if profile is public or private

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        # Encrypt the email before saving
        self.email = cipher_suite.encrypt(self.email.encode()).decode()
        super().save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance
        )  # Safely create the profile without duplicating


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):  # Ensure profile exists before trying to save
        instance.profile.save()


def validate_unique_nickname(nickname, instance=None):
    if instance:
        # Exclude the current instance from the uniqueness check
        if Profile.objects.filter(nickname=nickname).exclude(pk=instance.pk).exists():
            raise ValidationError(f"Nickname '{nickname}' is already taken.")
    else:
        if Profile.objects.filter(nickname=nickname).exists():
            raise ValidationError(f"Nickname '{nickname}' is already taken.")


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)

    def clean(self):
        validate_unique_nickname(self.nickname, instance=self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
