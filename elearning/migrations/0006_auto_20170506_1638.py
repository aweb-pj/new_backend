# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 08:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0005_nodehomework_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='homework_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='elearning.HomeworkAnswer'),
        ),
        migrations.AlterField(
            model_name='material',
            name='node_material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='elearning.NodeMaterial'),
        ),
        migrations.AlterField(
            model_name='question',
            name='node_homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='elearning.NodeHomework'),
        ),
    ]
