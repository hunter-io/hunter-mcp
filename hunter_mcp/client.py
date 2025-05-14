from typing import Optional, Dict, Any
import httpx
import os


class HunterClientError(Exception):
    """Exception raised for errors in the Hunter API client."""
    pass

class HunterAPIClient:
    """
    A client wrapper class for interacting with the Hunter API.
    
    This class handles authentication and provides methods for making
    requests to Hunter API endpoints.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.hunter.io/v2"):
        """
        Initialize the Hunter API client.
        
        Args:
            api_key: The Hunter API key. If not provided, will try to get from environment variable.
            base_url: The Hunter API base URL (default: https://api.hunter.io/v2)
        """
        
        self.api_key = api_key or os.getenv("HUNTER_API_KEY")
        self.base_url = base_url.rstrip("/")
        self._client: Optional[httpx.AsyncClient] = None

        if not self.api_key:
            raise HunterClientError("Hunter API key is required. Set HUNTER_API_KEY environment variable or pass it to the constructor.")
    
    async def __aenter__(self):
        """Creates a new HTTP session when entering the context."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            params={"api_key": self.api_key},
            headers={"X-SOURCE": "hunter-mcp"},
            timeout=30.0
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the HTTP session when exiting the context."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs a GET request to the specified endpoint.
        
        Args:
            endpoint: endpoint path (without leading slash)
            params: Additional request parameters
            
        Returns:
            The JSON response from the API.
            
        Raises:
            httpx.HTTPError: In case of HTTP error
        """
        if not self._client:
            raise RuntimeError("The client must be used in an async with context")
        
        response = await self._client.get(
            f"/{endpoint.lstrip('/')}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs a POST request to the specified endpoint.
        
        Args:
            endpoint: endpoint path (without leading slash)
            params: Additional request parameters
            
        Returns:
            The JSON response from the API.
            
        Raises:
            httpx.HTTPError: In case of HTTP error
        """
        if not self._client:
            raise RuntimeError("The client must be used in an async with context")
        
        response = await self._client.post(
            f"/{endpoint.lstrip('/')}",
            json=params
        )
        response.raise_for_status()
        return response.json()