# Generated by Django 4.0.1 on 2022-07-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('uk', 'uk')], max_length=100)),
                ('category', models.CharField(choices=[('News', 'News'), ('Entertainment', 'Entertainment'), ('Politics', 'Politics'), ('Dating', 'Dating')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WebListingTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('logo', models.FileField(upload_to='logos')),
            ],
        ),
    ]
