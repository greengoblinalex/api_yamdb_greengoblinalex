# Generated by Django 3.2 on 2023-04-27 09:23

from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256)),
                ('slug', models.SlugField(unique=True, validators=[reviews.validators.validate_alphanumeric])),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256)),
                ('slug', models.SlugField(unique=True, validators=[reviews.validators.validate_alphanumeric])),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('score', models.IntegerField(validators=[reviews.validators.score_validator])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256)),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('rating', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.category')),
            ],
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_genres', to='reviews.genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_genres', to='reviews.title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genres',
            field=models.ManyToManyField(through='reviews.TitleGenre', to='reviews.Genre'),
        ),
    ]
