from django.db.models.signals import post_save, post_init

from django_view_hierarchy.models import DjangoViewHiearchyEvent
from django_view_hierarchy.helpers import ModelChangeDetector

def post_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    event = DjangoViewHiearchyEvent(
        content_object=instance,
        is_creation=created,
    )
    event.save()


def post_init_handler(sender, **kwargs):
    instance = kwargs['instance']
    instance.changes = ModelChangeDetector(instance)

def register_all(model_classes):
    for model_class in model_classes:
        post_save.connect(post_save_handler, sender=model_class)
        post_init.connect(post_init_handler, sender=model_class)
