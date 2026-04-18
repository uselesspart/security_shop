from django.apps import apps as global_apps
from django.contrib.auth.management import create_permissions
from django.db import migrations


MODERATOR_GROUP_NAME = 'Moderator'
PRODUCT_PERMISSIONS = [
    'add_product',
    'change_product',
    'delete_product',
    'view_product',
]


def create_moderator_group(apps, schema_editor):
    products_config = global_apps.get_app_config('products')
    create_permissions(products_config, apps=apps, verbosity=0)

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    product_ct = ContentType.objects.get(app_label='products', model='product')
    perms = Permission.objects.filter(
        content_type=product_ct,
        codename__in=PRODUCT_PERMISSIONS,
    )

    group, _ = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)
    group.permissions.set(perms)


def remove_moderator_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name=MODERATOR_GROUP_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_moderator_group, remove_moderator_group),
    ]
