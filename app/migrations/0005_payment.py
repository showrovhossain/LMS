# Generated by Django 4.2.3 on 2023-08-10 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('canceled', 'Canceled')], default='paid', max_length=10)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.course')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.usercourse')),
            ],
        ),
    ]
