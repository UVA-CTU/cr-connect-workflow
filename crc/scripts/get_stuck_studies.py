"""Template for scripts"""
from crc import session
from crc.api.common import ApiError # noqa - this is our api error wrapper
from crc.models.study import StudyModel
from crc.scripts.script import Script # pylint disable=unable-to-import
from crc.services.protocol_builder import ProtocolBuilderService
from crc.services.study_service import StudyService


class GetStuckStudies(Script):
    """Template for creating scripts"""

    def get_description(self):
        """Method that returns a description of the script."""
        return """This is my description"""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Method to validate the script."""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):  # pylint: disable=unused-argument
        """Method to perform the task."""
        stuck_studies = StudyService().get_stuck_studies()
        return stuck_studies
