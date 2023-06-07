# Generated by Django 4.1.5 on 2023-06-07 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userpages', '0003_alter_plan_price'),
        ('editor', '0002_delete_qrcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='media/')),
                ('user', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='userpages.usermod')),
            ],
        ),
    ]
