from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from recipes.models import Recipe

User = get_user_model()


def delete_cover(instance, **kwargs):
    try:
        instance.cover.delete(save=False)
    except (ValueError, FileNotFoundError): 
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):

    # se está criando (não tem PK ainda), não faz nada
    if not instance.pk:
        return

    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    if not old_instance:
        return
    
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)