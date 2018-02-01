from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import BunnyApi, TextAPI
from django.conf import settings
from rest_framework.exceptions import ValidationError


class Readings(models.Model):
    """This class represents the readings model."""
    title = models.CharField(max_length=255, blank=False, unique=True)
    script = models.TextField(blank=False, null=False)
    test = models.IntegerField(blank=False,null=False)
    reads = models.TextField(blank=True, null=True)
    status_api = models.CharField(max_length=1, blank=False, default='N')
    status_reads = models.CharField(max_length=1, blank=False, default='N')
    project_error = models.TextField(blank=True, null=True)
    project_id = models.CharField(max_length=255, blank=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance"""
        return "{}".format(self.name)


@receiver(post_save, sender=Readings)
def create_speedy_project(sender, instance, **kwargs):
    post_save.disconnect(create_speedy_project, sender=sender)
    api_id = settings.BUNNY_API_ID
    api_key = settings.BUNNY_API_KEY
    wiki_api = TextAPI
    speed_project = BunnyApi(api_id, api_key)
    result_wiki = wiki_api.get_wikipedia_basic_info(instance.script)
    print(result_wiki)
    instance.script = result_wiki
    result_data = speed_project.create_speedy_project(instance)
    print(result_data)
    if 'project' in result_data:
        instance.status_api = 'S'
        instance.project_id = result_data['project']['id']
        instance.reads = result_data['project']['reads']
    elif 'error' in result_data:
        instance.status_api = 'E'
        instance.project_error = result_data
        raise ValidationError(result_data)

    instance.save()
    post_save.connect(create_speedy_project, sender=sender)