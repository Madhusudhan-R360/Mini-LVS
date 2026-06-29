from celery import Celery

celery_app = Celery(
    "lvs_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# ✅ VERY IMPORTANT - register tasks
celery_app.conf.imports = ("app.tasks",)