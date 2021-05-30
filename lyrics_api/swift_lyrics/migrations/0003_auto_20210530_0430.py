# Generated by Django 3.2 on 2021-05-30 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swift_lyrics', '0002_auto_20210413_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('first_year_active', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='year',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='lyric',
            name='votes',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='swift_lyrics.artist'),
        ),
    ]
