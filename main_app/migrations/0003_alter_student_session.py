# Generated by Django 4.2.1 on 2023-06-03 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.session'),
        ),
    ]
