# Generated by Django 5.2 on 2025-04-26 12:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teste', '0007_competicao_gerente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Convite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aceito', models.BooleanField(null=True)),
                ('jogador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites_recebidos', to=settings.AUTH_USER_MODEL)),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teste.time')),
            ],
        ),
    ]
