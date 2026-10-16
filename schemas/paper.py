from pydantic import BaseModel, Field


class Paper(BaseModel):
    paper_id: str = Field(
        description="Unique identifier for the paper from the source."
    )

    title: str

    authors: list[str] = Field(default_factory=list)

    year: int | None = None

    abstract: str | None = None

    doi: str | None = None

    url: str | None = None

    citation_count: int | None = None

    source: str = Field(
        description="Source from which the paper metadata was retrieved."
    )