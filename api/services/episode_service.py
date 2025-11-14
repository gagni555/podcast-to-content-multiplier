from sqlalchemy.orm import Session
from typing import List
from api.models import Episode, User
from api.schemas import EpisodeCreate


def create_episode_service(db: Session, episode: EpisodeCreate, user_id: int):
    """
    Create a new episode
    """
    db_episode = Episode(
        user_id=user_id,
        title=episode.title,
        audio_url=episode.audio_url,
        duration=episode.duration,
        file_size=episode.file_size,
        file_format=episode.file_format,
        generate_blog=episode.generate_blog,
        generate_social=episode.generate_social,
        generate_newsletter=episode.generate_newsletter,
        generate_show_notes=episode.generate_show_notes,
        generate_quote_graphics=episode.generate_quote_graphics
    )
    
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    
    return db_episode


def get_episodes_service(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Get episodes for a specific user
    """
    return db.query(Episode).filter(Episode.user_id == user_id).offset(skip).limit(limit).all()


def get_episode_service(db: Session, episode_id: int, user_id: int):
    """
    Get a specific episode by ID for a specific user
    """
    return db.query(Episode).filter(Episode.id == episode_id, Episode.user_id == user_id).first()