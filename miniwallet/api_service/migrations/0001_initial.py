# Generated by Django 3.2 on 2021-04-22 08:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(default=uuid.UUID('d7229928-a346-11eb-abd1-8c554a970c06'), max_length=50, primary_key=True, serialize=False)),
                ('owned_by', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('E', 'Enabled'), ('D', 'Disabled')], default='D', max_length=10)),
                ('changed_at', models.DateTimeField()),
                ('balance', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.CharField(default=uuid.UUID('d7229929-a346-11eb-8712-8c554a970c06'), max_length=50, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=20)),
                ('transaction_time', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('reference_id', models.CharField(max_length=50, unique=True)),
                ('transaction_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_service.account')),
            ],
        ),
    ]