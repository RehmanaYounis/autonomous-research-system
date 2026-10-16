from typing import Any

import httpx

from schemas.paper import Paper
from tools.literature.base import LiteratureSearchProvider


class OpenAlexProvider(LiteratureSearchProvider):

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self, timeout: float = 30.0):
        self.client = httpx.Client(timeout=timeout)

    def search(
        self,
        query: str,
        *,
        max_results: int = 20,
    ) -> list[Paper]:

        response = self.client.get(
            self.BASE_URL,
            params={
                "search": query,
                "per-page": max_results,
            },
        )

        response.raise_for_status()

        data = response.json()

        return [
            self._to_paper(work)
            for work in data.get("results", [])
        ]

    @staticmethod
    def _to_paper(work: dict[str, Any]) -> Paper:

        authors = [
            authorship["author"]["display_name"]
            for authorship in work.get("authorships", [])
            if authorship.get("author")
        ]

        doi = work.get("doi")

        if doi:
            doi = doi.removeprefix("https://doi.org/")

        primary_location = work.get("primary_location") or {}

        return Paper(
            paper_id=work["id"],
            title=work.get("title", ""),
            authors=authors,
            year=work.get("publication_year"),
            abstract=OpenAlexProvider._reconstruct_abstract(
                work.get("abstract_inverted_index")
            ),
            doi=doi,
            url=primary_location.get("landing_page_url"),
            citation_count=work.get("cited_by_count"),
            source="openalex",
        )

    @staticmethod
    def _reconstruct_abstract(
        inverted_index: dict[str, list[int]] | None,
    ) -> str | None:

        if not inverted_index:
            return None

        words_by_position = {}

        for word, positions in inverted_index.items():
            for position in positions:
                words_by_position[position] = word

        return " ".join(
            words_by_position[position]
            for position in sorted(words_by_position)
        )

if __name__ == "__main__":
    provider = OpenAlexProvider()

    papers = provider.search(
        query="reinforcement learning robotic grasping unseen objects",
        max_results=5,
    )

    print(f"\nFound {len(papers)} papers")

    for paper in papers:
        print("\n" + "=" * 80)
        print("TITLE:", paper.title)
        print("YEAR:", paper.year)
        print("AUTHORS:", paper.authors)
        print("DOI:", paper.doi)
        print("CITATIONS:", paper.citation_count)
        print("SOURCE:", paper.source)

        if paper.abstract:
            print("ABSTRACT:", paper.abstract[:300], "...")
        else:
            print("ABSTRACT: Not available")