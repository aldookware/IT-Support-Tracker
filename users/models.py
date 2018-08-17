from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse

import uuid


class Status(Enum):
    PENDING = 1
    SCHEDULED = 2
    DONE = 3
    CLOSED = 4
    OVERDUE = 5
    REVIEW = 6

    @property
    def human_name(self):
        names = {
            'PENDING': 'Pending',
            'SCHEDULED': 'Scheduled',
            'DONE': 'Done',
            'CLOSED': 'Closed',
            'OVERDUE': 'Overdue',
            'REVIEW': 'Review',
        }

        return names[self.name]


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    is_engineer = models.BooleanField('engineer', default=False)
    is_client_user = models.BooleanField('client_user', default=False)


class Engineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Engineer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, *args, **kwargs):
    instance.engineer.save()

    # client
    # service
    # engineer

    # we have two users, engineer, client_users


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, )
    contact_person_first_name = models.CharField(
        max_length=140, null=True, blank=True)
    contact_person_last_name = models.CharField(
        max_length=140, null=True, blank=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=300, blank=False)
    modified_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # return reverse_lazy(
        #     'client-api:detail',
        #     kwargs={
        #         'pk': self.id
        #     }
        # )
        pass

    def __str__(self):
        return str(self.title)


@receiver(pre_save, sender=Client)
def update_slug_field(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


class ClientUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    department = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        # return reverse_lazy(
        #     'clients:client-user-detail',
        #     kwargs={
        #         'user': self.user.pk
        #     }
        # )
        pass

    def __str__(self):
        return str(self.user.first_name)


class Issue(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    subject = models.CharField(max_length=140, null=True, blank=True)  # subject or summary if the issue
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # client who reported the issue
    status = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in Status],
        default=Status.PENDING.name)  # status of the issue, pending, resolved, etc
    expected_date = models.DateField(null=True)  # expected resolution date
    date_resolved = models.DateTimeField(null=True)
    issue_description = models.TextField()  # dated issue was resolved
    created_at = models.DateTimeField(auto_now_add=True)  # when the issue was created
    created_by = models.ForeignKey(User)  # user who created the issue
    modified_at = models.DateTimeField(auto_now=True)  # last modified time

    class Meta:
        ordering = ('-created_at',)


class IssueLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    Issue = models.OneToOneField(Issue, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in Status],
        default=Status.PENDING.name)
    log_by = models.ForeignKey(User)
