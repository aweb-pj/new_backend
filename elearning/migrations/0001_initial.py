# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import elearning.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('material_name', models.CharField(max_length=100)),
                ('material_file', models.FileField(upload_to=elearning.models.get_file_path)),
            ],
        ),
        migrations.CreateModel(
            name='NodeHomework',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('node_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NodeMaterial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('node_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('TEXT', 'TextQuestion'), ('CHOICE', 'ChoiceQuestion')], max_length=6)),
                ('question', models.CharField(max_length=100)),
                ('A', models.CharField(max_length=100, null=True)),
                ('B', models.CharField(max_length=100, null=True)),
                ('C', models.CharField(max_length=100, null=True)),
                ('D', models.CharField(max_length=100, null=True)),
                ('answer', models.CharField(max_length=100, null=True)),
                ('node_homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning.NodeHomework')),
            ],
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tree', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(db_index=True, max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('STUDENT', 'Student'), ('TEACHER', 'Teacher')], max_length=7)),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='node_material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning.NodeMaterial'),
        ),
        migrations.AddField(
            model_name='homeworkanswer',
            name='node_homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning.NodeHomework'),
        ),
        migrations.AddField(
            model_name='homeworkanswer',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning.User'),
        ),
        migrations.AddField(
            model_name='answer',
            name='homework_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning.HomeworkAnswer'),
        ),
    ]
