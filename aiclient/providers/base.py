from typing import Any, Dict, List, Optional, Protocol, Tuple, Union

from ..data_types import BaseMessage, ModelResponse, StreamChunk


class Provider(Protocol):
    """
    Protocol that defines how to interact with an AI provider.
    It handles standardizing the request payload and parsing the response.
    """

    @property
    def base_url(self) -> str:
        """Return the base URL for this provider."""
        ...

    @property
    def headers(self) -> Dict[str, str]:
        """Return the headers for this provider."""
        ...

    def prepare_request(
        self,
        model: str,
        messages: List[BaseMessage],
        tools: List[Any] = None,
        stream: bool = False,
        response_schema: Optional[Dict[str, Any]] = None,
        strict: bool = False,
        temperature: float = None,
        max_tokens: int = None,
        top_p: float = None,
        top_k: int = None,
        stop: Union[str, List[str]] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Prepare the endpoint and JSON payload for the request.
        Returns (endpoint, json_payload).
        """
        ...

    def parse_response(self, response_data: Dict[str, Any]) -> ModelResponse:
        """Parse the raw response into a standardized ModelResponse."""
        ...

    def parse_stream_chunk(self, chunk: Dict[str, Any]) -> Optional[StreamChunk]:
        """Parse a stream chunk into a standardized StreamChunk."""
        ...

    def prepare_embeddings_request(
        self, model: str, input: Union[str, List[str]]
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Prepare request for embeddings.
        Returns (endpoint, json_payload).
        """
        ...

    def parse_embeddings_response(
        self, response_data: Dict[str, Any]
    ) -> Union[List[float], List[List[float]]]:
        """
        Parse the raw response into embeddings.
        Returns list of floats or list of list of floats.
        """
        ...
