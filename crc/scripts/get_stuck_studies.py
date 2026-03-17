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
        stuck_studies = []
        pr_complete_studies = session.query(StudyModel).filter(
            StudyModel.progress_status == 'pre_review_complete').all()

        for pr_complete_study in pr_complete_studies:
            prc_study_id = pr_complete_study.id
            stuck_study_url = StudyService().get_study_url(prc_study_id)
            irb_info = ProtocolBuilderService.get_irb_info(prc_study_id)[0]
            irb_status = irb_info['IRB_STATUS']
            # if irb_status and irb_status != 'pre_review_complete':
            # print(f"Study {stuck_id}: Irb status: {irb_status}")
            stuck_studies.append({'id': prc_study_id,
                                  'short_title':pr_complete_study.short_title,
                                  'study_url': stuck_study_url,
                                  'irb_status': irb_status}
                                 )
        return stuck_studies
