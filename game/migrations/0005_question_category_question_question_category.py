# Generated by Django 4.2.5 on 2023-09-25 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_alter_response_partner1_alter_response_partner2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('negative_mark_to', models.CharField(max_length=1, verbose_name=(('m', 'Male'), ('f', 'Female')))),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.question_category'),
        ),
    ]
