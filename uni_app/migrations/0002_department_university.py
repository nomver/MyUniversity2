# Generated by Django 3.1.2 on 2020-10-25 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uni_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='university',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='uni_app.university'),
            preserve_default=False,
        ),
    ]