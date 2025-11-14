import asyncio
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from api.models import Episode, Transcript
from api.services import (
    transcription_service,
    content_generation_service,
    update_processing_job_status
)


async def process_episode_content(db: Session, episode_id: int):
    """
    Main workflow to process an episode: transcribe -> generate content -> update status
    """
    # Get the episode from the database
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not episode:
        raise ValueError(f"Episode with ID {episode_id} not found")
    
    # Update job status to processing
    update_processing_job_status(db, episode_id, "processing", 10)
    
    try:
        # Step 1: Transcribe the audio
        print(f"Starting transcription for episode {episode_id}")
        transcript_data = await transcription_service.transcribe_audio(episode.audio_url)
        
        # Create transcript record
        transcript = Transcript(
            episode_id=episode.id,
            text=transcript_data["text"],
            segments_json=str(transcript_data["segments"]),  # In real app, use proper JSON
            speakers_json=str(transcript_data["speakers"]),  # In real app, use proper JSON
            word_count=transcript_data["word_count"]
        )
        db.add(transcript)
        db.commit()
        
        # Update progress
        update_processing_job_status(db, episode_id, "processing", 40)
        
        # Step 2: Generate content based on user preferences
        print(f"Starting content generation for episode {episode_id}")
        
        # Generate blog post if requested
        if episode.generate_blog:
            print("Generating blog post...")
            blog_content = await content_generation_service.generate_blog_post(episode, transcript.text)
            # In a real implementation, we would save this to the database
            
        # Update progress
        update_processing_job_status(db, episode_id, "processing", 60)
        
        # Generate social media content if requested
        if episode.generate_social:
            print("Generating social media content...")
            social_content = await content_generation_service.generate_social_media_content(episode, transcript.text)
            # In a real implementation, we would save this to the database
            
        # Update progress
        update_processing_job_status(db, episode_id, "processing", 80)
        
        # Generate newsletter content if requested
        if episode.generate_newsletter:
            print("Generating newsletter content...")
            newsletter_content = await content_generation_service.generate_newsletter_content(episode, transcript.text)
            # In a real implementation, we would save this to the database
            
        # Generate show notes if requested
        if episode.generate_show_notes:
            print("Generating show notes...")
            show_notes = await content_generation_service.generate_show_notes(episode, transcript.text)
            # In a real implementation, we would save this to the database
            
        # Update progress to complete
        update_processing_job_status(db, episode_id, "completed", 100)
        
        # Update episode status
        episode.status = "completed"
        episode.processed_at = datetime.utcnow()
        db.commit()
        
        print(f"Completed processing for episode {episode_id}")
        return {"status": "success", "episode_id": episode_id}
        
    except Exception as e:
        # Update job status to failed
        update_processing_job_status(db, episode_id, "failed", 0, str(e))
        episode.status = "failed"
        db.commit()
        print(f"Failed processing for episode {episode_id}: {str(e)}")
        raise e