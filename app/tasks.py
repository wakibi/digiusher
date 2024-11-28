from app.integrations.aws import import_aws_data
from .extensions import scheduler

@scheduler.task(
    "cron",
    id="aws_data_update",
    day_of_week='*',
    max_instances=1,
    hour="00",
)
def task1():
    """
    Added when app starts.
    """
    print("Running AWS data update!")
    with scheduler.app.app_context():
        import_aws_data()