from abc import ABC, abstractmethod

from schemas.paper import Paper


class LiteratureSearchProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        *,
        max_results: int = 20,
    ) -> list[Paper]:
        """Search for papers and return normalized Paper objects."""
        pass