# Generated by Django 4.2.8 on 2023-12-18 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monolith', '0003_alter_vote_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
