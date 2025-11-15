"""YouTube transcript provider with Whisper fallback."""
import re
import tempfile
from pathlib import Path
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import yt_dlp
from loguru import logger
from ...config import settings


class YouTubeProvider:
    """Provides transcripts from YouTube videos."""
    
    def __init__(self):
        self.whisper_mode = settings.whisper_mode
        self.whisper_model = settings.whisper_model
    
    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL.
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already a video ID
        return url
    
    async def from_youtube(self, video_id: str) -> tuple[str, dict]:
        """Get transcript from YouTube video.
        
        Args:
            video_id: YouTube video ID or URL
            
        Returns:
            Tuple of (transcript text, metadata dict)
        """
        video_id = self._extract_video_id(video_id)
        logger.info(f"Getting transcript for video: {video_id}")
        
        # Try youtube-transcript-api first
        try:
            transcript, metadata = await self._get_transcript_api(video_id)
            logger.info("Successfully got transcript from YouTube API")
            return transcript, metadata
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logger.warning(f"No transcript available via API: {e}, falling back to Whisper")
            if self.whisper_mode == "disabled":
                raise ValueError(
                    f"No transcript available for this video and Whisper is disabled. "
                    f"Enable Whisper in settings or choose a video with captions."
                ) from e
            return await self._get_transcript_whisper(video_id)
        except Exception as e:
            logger.error(f"Unexpected error getting transcript via API: {e}")
            raise
    
    async def _get_transcript_api(self, video_id: str) -> tuple[str, dict]:
        """Get transcript using youtube-transcript-api.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Tuple of (transcript text, metadata dict)
        """
        # Run in thread pool since it's blocking
        loop = asyncio.get_event_loop()
        api = YouTubeTranscriptApi()
        
        def get_transcript():
            return api.fetch(video_id)
        
        fetched_transcript = await loop.run_in_executor(
            None,
            get_transcript
        )
        
        # Format transcript with timestamps
        lines = []
        timestamps = []
        
        for snippet in fetched_transcript.snippets:
            start = snippet.start
            text = snippet.text
            minutes = int(start // 60)
            seconds = int(start % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            
            lines.append(f"{timestamp} {text}")
            timestamps.append({
                "time": start,
                "timestamp": timestamp,
                "text": text
            })
        
        transcript = "\n".join(lines)
        metadata = {
            "has_timestamps": True,
            "timestamps": timestamps,
            "source": "youtube_api"
        }
        
        return transcript, metadata
    
    async def _get_transcript_whisper(self, video_id: str) -> tuple[str, dict]:
        """Get transcript using yt-dlp + Whisper.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Tuple of (transcript text, metadata dict)
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "audio.mp3"
            
            # Download audio with yt-dlp
            logger.info(f"Downloading audio for video: {video_id}")
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': str(audio_path.with_suffix('')),
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            }
            
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(
                    None,
                    self._download_audio,
                    video_id,
                    ydl_opts
                )
            except Exception as e:
                logger.error(f"Failed to download audio: {e}")
                raise ValueError(
                    f"Could not download video audio. This may be due to YouTube restrictions. "
                    f"Try a different video or check if Whisper is properly configured."
                ) from e
            
            # Transcribe with Whisper
            if self.whisper_mode == "local":
                transcript = await self._transcribe_local(audio_path)
            else:
                transcript = await self._transcribe_openai(audio_path)
            
            metadata = {
                "has_timestamps": False,
                "source": f"whisper_{self.whisper_mode}"
            }
            
            return transcript, metadata
    
    def _download_audio(self, video_id: str, ydl_opts: dict) -> None:
        """Download audio using yt-dlp (blocking)."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    async def _transcribe_local(self, audio_path: Path) -> str:
        """Transcribe audio using local Whisper model.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        import whisper
        
        logger.info(f"Transcribing with local Whisper model: {self.whisper_model}")
        
        loop = asyncio.get_event_loop()
        model = await loop.run_in_executor(
            None,
            whisper.load_model,
            self.whisper_model
        )
        
        result = await loop.run_in_executor(
            None,
            model.transcribe,
            str(audio_path)
        )
        
        return result["text"]
    
    async def _transcribe_openai(self, audio_path: Path) -> str:
        """Transcribe audio using OpenAI Whisper API.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        from openai import AsyncOpenAI
        
        logger.info("Transcribing with OpenAI Whisper API")
        
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        
        with open(audio_path, "rb") as audio_file:
            response = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        return response.text
