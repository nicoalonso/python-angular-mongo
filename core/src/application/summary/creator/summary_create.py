from src.domain.bus import DomainBus
from src.domain.summary import SummaryRepository, Summary, SummaryType
from src.domain.user import UserRepository
from .summary_create_payload import SummaryCreatePayload
from .summary_created_event import SummaryCreatedEvent


class SummaryCreate:
    """
    Use case for creating a summary.

    :ivar repo_summary: Summary repository
    :ivar repo_user: User repository
    """
    def __init__(
            self,
            repo_summary: SummaryRepository,
            repo_user: UserRepository,
            bus: DomainBus,
    ):
        self.repo_summary = repo_summary
        self.repo_user = repo_user
        self.bus = bus

    async def dispatch(self, payload: SummaryCreatePayload) -> Summary:
        """
        Dispatch the event to create a summary.

        :param payload: SummaryCreatePayload - Payload containing the URL and other information
        :return: Summary - Created summary
        """
        summary = await self.repo_summary.obtain_by_url(payload.url)
        if summary is not None:
            return summary

        type_ = SummaryType.try_from(payload.type)
        user = self.repo_user.obtain_user()
        summary = Summary.create(
            url=payload.url,
            type_=type_,
            created_by=user.name,
        )

        await self.repo_summary.save(summary)

        event = SummaryCreatedEvent(summary.id)
        await self.bus.dispatch(event)

        return summary
