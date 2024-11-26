# Generated by Django 4.2.5 on 2023-09-26 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0010_alter_registration_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='name',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='phone_no',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='relationship_started_year',
        ),
        migrations.AddField(
            model_name='registration',
            name='partner1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='partner2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner2', to=settings.AUTH_USER_MODEL),
        ),
    ]
