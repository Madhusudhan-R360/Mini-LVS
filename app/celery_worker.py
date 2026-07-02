from celery import Celery

celery_app = Celery(
    "lvs_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.imports = ("app.tasks",)

# ✅ Reliability improvement
celery_app.conf.task_acks_late = True

# ✅ Better task distribution
celery_app.conf.worker_prefetch_multiplier = 1

celery_app.conf.task_routes = {
    "app.tasks.process_order_task": {
        "queue": "orders_queue"
    }
}