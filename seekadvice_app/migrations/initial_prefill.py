from django.db import migrations

def prefill_service_areas(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ServiceAreas = apps.get_model('seekadvice_app', 'ServiceAreas')

    topics = [
        "Pandas",
        "Numpy",
        "sktime",
        "FastAPI",
        "Django",
        "PyTorch",
        "Dash"
        ]

    for topic in topics:
        themen = ServiceAreas(serviceareas = topic)
        themen.save()

def prefill_service_technology(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ServiceTechnology = apps.get_model('seekadvice_app', 'ServiceTechnology')

    topics = [
        "JavaScript",
        "CSS",
        "HTML",
        "Python",
        "Ruby",
        "Java",
        "Go",
        "PHP",
        "AWS",
        "GCP",
        "Azure",
        "Heroku"
        ]

    for topic in topics:
        themen = ServiceTechnology(servicetechnology = topic)
        themen.save()


class Migration(migrations.Migration):

    dependencies = [
        ('seekadvice_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(prefill_service_areas),
        migrations.RunPython(prefill_service_technology),
    ]