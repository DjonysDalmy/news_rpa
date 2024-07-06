from robocorp.tasks import task
from src.news import News
from src.logger import Logger


@task
def start():
    Logger.setup()
    try:
        News().start()
    except Exception as e:
        Logger.error(f"🚨 An error occurred: {e}")

if __name__ == "__main__":
    start()
