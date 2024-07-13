from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user1 = User.objects.create_superuser(
        username='admin',
        password='123456',
        email='admin@example.com'
    )
    user1.last_login = user1.date_joined
    user1.save()

    user2 = User.objects.create_user(
        username='peter',
        password='spiderman',
        email='peter@example.com'
    )
    user2.last_login = user2.date_joined
    user2.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequestHistory',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=20)),
                ('open', models.DecimalField(decimal_places=2, max_digits=10)),
                ('high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('close', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_users),
    ]
