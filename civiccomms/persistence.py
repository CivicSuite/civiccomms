from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civiccomms.meeting_summary import draft_meeting_summary
from civiccomms.source_review import review_sources


metadata = sa.MetaData()

source_review_records = sa.Table(
    "source_review_records",
    metadata,
    sa.Column("review_id", sa.String(36), primary_key=True),
    sa.Column("source_titles", sa.JSON(), nullable=False),
    sa.Column("citations", sa.JSON(), nullable=False),
    sa.Column("source_count", sa.Integer(), nullable=False),
    sa.Column("ready_for_draft", sa.Boolean(), nullable=False),
    sa.Column("missing_items", sa.JSON(), nullable=False),
    sa.Column("boundary", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccomms",
)

meeting_summary_records = sa.Table(
    "meeting_summary_records",
    metadata,
    sa.Column("summary_id", sa.String(36), primary_key=True),
    sa.Column("meeting_title", sa.String(500), nullable=False),
    sa.Column("actions", sa.JSON(), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("audience", sa.String(255), nullable=False),
    sa.Column("draft_points", sa.JSON(), nullable=False),
    sa.Column("required_review_steps", sa.JSON(), nullable=False),
    sa.Column("citations", sa.JSON(), nullable=False),
    sa.Column("boundary", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccomms",
)


@dataclass(frozen=True)
class StoredSourceReview:
    review_id: str
    source_titles: tuple[str, ...]
    citations: tuple[str, ...]
    source_count: int
    ready_for_draft: bool
    missing_items: tuple[str, ...]
    boundary: str
    created_at: datetime


@dataclass(frozen=True)
class StoredMeetingSummary:
    summary_id: str
    meeting_title: str
    actions: tuple[str, ...]
    title: str
    audience: str
    draft_points: tuple[str, ...]
    required_review_steps: tuple[str, ...]
    citations: tuple[str, ...]
    boundary: str
    created_at: datetime


class CommunicationsDraftRepository:
    """SQLAlchemy-backed source review and public draft records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civiccomms": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civiccomms"))
        metadata.create_all(self.engine)

    def create_source_review(
        self, *, source_titles: list[str], citations: list[str]
    ) -> StoredSourceReview:
        review = review_sources(source_titles=source_titles, citations=citations)
        stored = StoredSourceReview(
            review_id=str(uuid4()),
            source_titles=tuple(source_titles),
            citations=tuple(citations),
            source_count=review.source_count,
            ready_for_draft=review.ready_for_draft,
            missing_items=tuple(review.missing_items),
            boundary=review.boundary,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                source_review_records.insert().values(
                    review_id=stored.review_id,
                    source_titles=list(stored.source_titles),
                    citations=list(stored.citations),
                    source_count=stored.source_count,
                    ready_for_draft=stored.ready_for_draft,
                    missing_items=list(stored.missing_items),
                    boundary=stored.boundary,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_source_review(self, review_id: str) -> StoredSourceReview | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(source_review_records).where(source_review_records.c.review_id == review_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_source_review(row)

    def create_meeting_summary(
        self,
        *,
        meeting_title: str,
        actions: list[str],
        citations: list[str],
        audience: str = "residents",
    ) -> StoredMeetingSummary:
        draft = draft_meeting_summary(
            meeting_title=meeting_title,
            actions=actions,
            citations=citations,
            audience=audience,
        )
        stored = StoredMeetingSummary(
            summary_id=str(uuid4()),
            meeting_title=meeting_title,
            actions=tuple(actions),
            title=draft.title,
            audience=draft.audience,
            draft_points=tuple(draft.draft_points),
            required_review_steps=tuple(draft.required_review_steps),
            citations=tuple(draft.citations),
            boundary=draft.boundary,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                meeting_summary_records.insert().values(
                    summary_id=stored.summary_id,
                    meeting_title=stored.meeting_title,
                    actions=list(stored.actions),
                    title=stored.title,
                    audience=stored.audience,
                    draft_points=list(stored.draft_points),
                    required_review_steps=list(stored.required_review_steps),
                    citations=list(stored.citations),
                    boundary=stored.boundary,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_meeting_summary(self, summary_id: str) -> StoredMeetingSummary | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(meeting_summary_records).where(
                    meeting_summary_records.c.summary_id == summary_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_meeting_summary(row)


def _row_to_source_review(row: object) -> StoredSourceReview:
    data = dict(row)
    return StoredSourceReview(
        review_id=data["review_id"],
        source_titles=tuple(data["source_titles"]),
        citations=tuple(data["citations"]),
        source_count=data["source_count"],
        ready_for_draft=data["ready_for_draft"],
        missing_items=tuple(data["missing_items"]),
        boundary=data["boundary"],
        created_at=data["created_at"],
    )


def _row_to_meeting_summary(row: object) -> StoredMeetingSummary:
    data = dict(row)
    return StoredMeetingSummary(
        summary_id=data["summary_id"],
        meeting_title=data["meeting_title"],
        actions=tuple(data["actions"]),
        title=data["title"],
        audience=data["audience"],
        draft_points=tuple(data["draft_points"]),
        required_review_steps=tuple(data["required_review_steps"]),
        citations=tuple(data["citations"]),
        boundary=data["boundary"],
        created_at=data["created_at"],
    )
