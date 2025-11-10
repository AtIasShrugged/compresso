"""URL article text extraction."""
import httpx
from bs4 import BeautifulSoup
from readability import Document
from loguru import logger


class URLReader:
    """Extracts text content from article URLs."""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
    
    async def from_url(self, url: str) -> str:
        """Extract main article text from URL.
        
        Args:
            url: Article URL
            
        Returns:
            Extracted article text
            
        Raises:
            RuntimeError: If extraction fails
        """
        try:
            logger.info(f"Fetching URL: {url}")
            
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                html = response.text
            
            # Use readability to extract main content
            doc = Document(html)
            title = doc.title()
            content_html = doc.summary()
            
            # Parse with BeautifulSoup to get clean text
            soup = BeautifulSoup(content_html, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator="\n", strip=True)
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = "\n".join(lines)
            
            result = f"# {title}\n\n{text}"
            
            logger.info(f"Extracted {len(result)} characters from URL")
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching URL: {e}")
            raise RuntimeError(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            logger.error(f"Error extracting text from URL: {e}")
            raise RuntimeError(f"Failed to extract text: {str(e)}")
