# Generated by Django 4.1.3 on 2022-11-08 18:39

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ("electronics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="networkobject",
            name="location_city",
            field=smart_selects.db_fields.ChainedForeignKey(
                auto_choose=True,
                chained_field="country",
                chained_model_field="city",
                on_delete=django.db.models.deletion.CASCADE,
                to="electronics.city",
            ),
        ),
    ]