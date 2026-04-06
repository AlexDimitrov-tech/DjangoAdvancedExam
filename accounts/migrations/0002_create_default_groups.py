from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    member, _ = Group.objects.get_or_create(name='Member')
    admin_group, _ = Group.objects.get_or_create(name='CommunityAdmin')

    member_perm_codenames = {
        'add_game', 'change_game', 'delete_game', 'view_game',
        'add_review', 'change_review', 'delete_review', 'view_review',
        'add_rentalrequest', 'change_rentalrequest', 'delete_rentalrequest', 'view_rentalrequest',
    }

    admin_perm_codenames = member_perm_codenames | {
        'add_category', 'change_category', 'delete_category', 'view_category',
    }

    member.permissions.set(Permission.objects.filter(codename__in=member_perm_codenames))
    admin_group.permissions.set(Permission.objects.filter(codename__in=admin_perm_codenames))


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Member', 'CommunityAdmin']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('catalog', '0002_game_cover_image_game_favorited_by'),
        ('rentals', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_code=remove_groups),
    ]
