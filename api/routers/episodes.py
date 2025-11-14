from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

from api.database import get_db
from api.models import Episode, User, Transcript, ProcessingJob
from api.schemas import Episode as EpisodeSchema, EpisodeCreate, EpisodeUpdate
from api.utils.auth import oauth2_scheme, get_current_user
from api.services import (
    create_episode_service,
    get_episodes_service,
    get_episode_service,
    generate_unique_filename,
    validate_file_type,
    validate_file_size,
    get_file_size_limit_mb
)
from api.workers.tasks import process_episode_task

router = APIRouter()


@router.post("/", response_model=EpisodeSchema)
def create_episode(
    title: str,
    generate_blog: bool = True,
    generate_social: bool = True,
    generate_newsletter: bool = True,
    generate_show_notes: bool = True,
    generate_quote_graphics: bool = True,
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Upload a new podcast episode and create processing job
    """
    # Get current user from token
    current_user = get_current_user(token=token, db=db)
    user_id = current_user.id
    
    # Validate file type
    if not validate_file_type(audio_file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only MP3, WAV, M4A, and FLAC files are allowed."
        )
    
    # Validate file size
    # Note: This is a basic check. For production, implement proper file size validation
    audio_file.file.seek(0, 2)  # Seek to end of file
    file_size = audio_file.file.tell()
    audio_file.file.seek(0)  # Reset file pointer to beginning
    
    if not validate_file_size(file_size):
        max_size_mb = get_file_size_limit_mb()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {max_size_mb}MB limit."
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(audio_file.filename)
    file_path = f"uploads/{unique_filename}"
    
    # TODO: Implement actual file upload to S3 or local storage
    # For now, we'll just store the path as a placeholder
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(audio_file.file, buffer)
    
    # Create episode data
    episode_data = EpisodeCreate(
        title=title,
        audio_url=file_path, # This should be the actual URL to the file
        file_size=file_size,
        file_format=os.path.splitext(audio_file.filename)[1][1:],  # Remove the dot from extension
        duration=None,  # To be calculated later
        generate_blog=generate_blog,
        generate_social=generate_social,
        generate_newsletter=generate_newsletter,
        generate_show_notes=generate_show_notes,
        generate_quote_graphics=generate_quote_graphics
    )
    
    # Create episode using service
    db_episode = create_episode_service(db, episode_data, user_id)
    
    # Create initial processing job
    processing_job = ProcessingJob(
        episode_id=db_episode.id,
        job_type="all",  # Process all content types
        status="pending"
    )
    
    db.add(processing_job)
    db.commit()
    
    # Trigger background processing
    process_episode_task.delay(db_episode.id)
    
    return db_episode


@router.get("/", response_model=List[EpisodeSchema])
def get_episodes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Get list of episodes for the authenticated user
    """
    # Get current user from token
    current_user = get_current_user(token=token, db=db)
    user_id = current_user.id
    
    episodes = get_episodes_service(db, user_id, skip, limit)
    return episodes


@router.get("/{episode_id}", response_model=EpisodeSchema)
def get_episode(
    episode_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Get a specific episode by ID
    """
    # Get current user from token
    current_user = get_current_user(token=token, db=db)
    user_id = current_user.id
    
    episode = get_episode_service(db, episode_id, user_id)
    
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episode not found"
        )
    
    return episode


@router.put("/{episode_id}", response_model=EpisodeSchema)
def update_episode(
    episode_id: int,
    episode_update: EpisodeUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Update a specific episode
    """
    # Get current user from token
    current_user = get_current_user(token=token, db=db)
    user_id = current_user.id
    
    episode = get_episode_service(db, episode_id, user_id)
    
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episode not found"
        )
    
    # Update fields
    for field, value in episode_update.dict(exclude_unset=True).items():
        setattr(episode, field, value)
    
    db.commit()
    db.refresh(episode)
    
    return episode


@router.delete("/{episode_id}")
def delete_episode(
    episode_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Delete a specific episode
    """
    # Get current user from token
    current_user = get_current_user(token=token, db=db)
    user_id = current_user.id
    
    episode = get_episode_service(db, episode_id, user_id)
    
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episode not found"
        )
    
    db.delete(episode)
    db.commit()
    
    return {"message": "Episode deleted successfully"}