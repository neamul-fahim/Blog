from django.db import models
from user_management.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(post_migrate)
def group_permissions(sender, **kwargs):

    content_type = ContentType.objects.get_for_model(Article)

    author_permissions = [
        Permission.objects.get_or_create(
            codename='add_article', name='Can add article', content_type=content_type)[0],
        Permission.objects.get_or_create(
            codename='change_article', name='Can change article', content_type=content_type)[0],
        Permission.objects.get_or_create(
            codename='delete_article', name='Can delete article', content_type=content_type)[0],
        Permission.objects.get_or_create(
            codename='view_article', name='Can view article', content_type=content_type)[0],
    ]
    author_group, created = Group.objects.get_or_create(name='Author')
    author_group.permissions.set(author_permissions)

    moderator_permissions = [
        Permission.objects.get_or_create(
            codename='delete_article', name='Can delete article', content_type=content_type)[0],
        Permission.objects.get_or_create(
            codename='ban_author', name='Can ban author', content_type=content_type)[0],
        Permission.objects.get_or_create(
            codename='unban_author', name='Can unban author', content_type=content_type)[0],
    ]
    moderator_group, created = Group.objects.get_or_create(name='Moderator')
    moderator_group.permissions.set(moderator_permissions)
