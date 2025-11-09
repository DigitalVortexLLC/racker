# Generated manually for UUID field on Site model
import uuid
from django.db import migrations, models


def generate_uuids(apps, schema_editor):
    """Generate UUIDs for existing Site records"""
    Site = apps.get_model('api', 'Site')
    for site in Site.objects.all():
        site.uuid = uuid.uuid4()
        site.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_device_power_ports_used'),
    ]

    operations = [
        # Step 1: Add uuid field as nullable first
        migrations.AddField(
            model_name='site',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True, blank=True),
        ),
        # Step 2: Generate UUIDs for existing records
        migrations.RunPython(generate_uuids, migrations.RunPython.noop),
        # Step 3: Make the field non-nullable and unique
        migrations.AlterField(
            model_name='site',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True),
        ),
    ]
