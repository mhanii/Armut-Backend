import random
import string

from django.utils.text import slugify





def random_string_generator(instance, chars = string.ascii_lowercase+string.digits):
    return "".join(random.choice(chars) for _ in range(4))


def unique_slug_generator(instance,new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.description)
        if len(slug) > 50:
            slug = slug[0:50]

    modelClass = instance.__class__

    slugexist = modelClass.objects.filter(link=slug).exists()
    if slugexist:
        new_slug = "{slug}-{randstr}".format(
            slug = slug,
            randstr = random_string_generator(instance)
        )
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug