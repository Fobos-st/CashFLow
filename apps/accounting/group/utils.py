from uuid import uuid4

from pytils.translit import slugify


def unique_slugify(instance, slug, slug_field):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    if not slug_field:
        slug_field = slugify(slug)
    if model.objects.filter(slug=slug_field).exclude(id=instance.id).exists():
        slug_field = f'{slugify(slug)}-{uuid4().hex[:6]}'
    return slug_field


def generate_unique_code(instance) -> str:
    """
    Генерирует уникальный код для GroupAccount
    """
    model = instance.__class__
    code_field = uuid4().hex[:6]
    if model.objects.filter(slug=code_field).exclude(id=instance.id).exists():
        return generate_unique_code(instance)
    return code_field
