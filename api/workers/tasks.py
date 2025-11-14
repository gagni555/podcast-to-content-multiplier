import asyncio
from .celery_app import celery_app
from api.database import SessionLocal
from api.workflows import process_episode_content


@celery_app.task
def process_episode_task(episode_id: int):
    """
    Celery task to process an episode in the background
    """
    # Create a new database session for this task
    db = SessionLocal()
    try:
        # Run the content processing workflow in an async context
        result = asyncio.run(process_episode_content(db, episode_id))
        return result
    except Exception as e:
        # Log the error and re-raise
        print(f"Error processing episode {episode_id}: {str(e)}")
        raise e
    finally:
        # Close the database session
        db.close()