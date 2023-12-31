# Generated by Django 4.1.7 on 2023-04-17 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_type',
            field=models.CharField(choices=[('Article', (('PL', 'Policy'), ('EC', 'Economic'), ('SP', 'Sport'), ('ED', 'Education'), ('CL', 'Culture'))), ('News', (('PL', 'Policy'), ('EC', 'Economic'), ('SP', 'Sport'), ('ED', 'Education'), ('CL', 'Culture')))], max_length=300),
        ),
    ]
