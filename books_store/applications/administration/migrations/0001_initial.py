# Generated by Django 4.2 on 2023-05-05 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0002_alter_order_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('investment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('target', models.DecimalField(decimal_places=2, max_digits=10)),
                ('highest_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='highest_sale', to='order.order')),
            ],
            options={
                'verbose_name': 'CashSummary',
                'verbose_name_plural': 'CashSummaries',
            },
        ),
    ]