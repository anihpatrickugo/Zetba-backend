from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

    def ready(self):
        # This ensures your index.py files are loaded
        # and models are registered with Algolia
        import events.index
