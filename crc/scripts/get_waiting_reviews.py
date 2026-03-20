"""Template for scripts"""
from crc import session
from crc.api.common import ApiError # noqa - this is our api error wrapper
from crc.models.data_store import DataStoreModel
from crc.models.study import StudyModel
from crc.scripts.script import Script # pylint disable=unable-to-import
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

from crc.services.study_service import StudyService


class GetWaitingReviews(Script):
    """Template for creating scripts"""

    def get_description(self):
        """Method that returns a description of the script."""
        return """This is my description"""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Method to validate the script."""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    @staticmethod
    def do_waiting_review_query():
        cutoff = datetime.now(timezone.utc) - timedelta(weeks=2)

        aggregated = (
            session.query(
                DataStoreModel.study_id.label("study_id"),
                func.max(DataStoreModel.value).filter(DataStoreModel.key == "sdsDC_request_id").label("request_id"),
                func.max(DataStoreModel.value).filter(DataStoreModel.key == "sdsDC_reminder_id").label("reminder_id"),
                func.max(DataStoreModel.value).filter(DataStoreModel.key == "sdsDC_approval_id").label("approval_id"),
            )
            .filter(DataStoreModel.key.in_(["sdsDC_request_id", "sdsDC_reminder_id", "sdsDC_approval_id"]))
            .group_by(DataStoreModel.study_id)
            .subquery()
        )

        query_results = (
            session.query(
                aggregated.c.study_id,
                StudyModel.short_title,
                aggregated.c.request_id,
                aggregated.c.reminder_id,
                aggregated.c.approval_id,
                DataStoreModel.last_updated,
            )
            .join(StudyModel, StudyModel.id == aggregated.c.study_id)
            .join(
                DataStoreModel,
                (DataStoreModel.study_id == aggregated.c.study_id)
                & (DataStoreModel.key == "sdsDC_reminder_id"),
            )
            .filter(aggregated.c.request_id.isnot(None))
            .filter(aggregated.c.reminder_id.isnot(None))
            .filter(aggregated.c.approval_id.is_(None))
            .filter(DataStoreModel.last_updated < cutoff)
        ).all()
        return query_results

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):  # pylint: disable=unused-argument
        """Method to perform the task."""

        waiting_reviews = []
        waiting_review_results = self.do_waiting_review_query()
        for review in waiting_review_results:
            review_dict = {'study_id': review[0],
                           'short_title': review[1],
                           'study_url': StudyService().get_study_url(review[0]),
                           'request_id': review[2],
                           'reminder_id': review[3],
                           'approval_id': review[4],
                           'last_updated': review[5]
                           }
            waiting_reviews.append(review_dict)

        return waiting_reviews
