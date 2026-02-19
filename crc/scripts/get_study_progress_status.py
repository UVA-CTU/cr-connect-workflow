from crc import session
from crc.models.study import StudyModel
from crc.scripts.script import Script
from crc.services.data_store_service import DataStoreBase


class GetStudyProgressStatus(Script):

    def get_description(self):
        return """
        Get the progress status of the current study. 
        Progress status is only set when `status` is `in_progress`. 
        Progress status can be one of `in_progress`, `submitted_for_pre_review`, `in_pre_review`, `returned_from_pre_review`, `pre_review_complete`, `agenda_date_set`, `approved`, `approved_with_conditions`, `deferred`, or `disapproved`.
        """

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):
        # IRB is not using the built-in Return to PI feature
        # This hack allows us to display the Resubmission workflow
        local_return_to_pi = DataStoreBase().get_data_common('study',
                                                 'sds_toggle_resubmission',
                                                 study_id,
                                                 None,
                                                 None,
                                                 None)
        if local_return_to_pi == 'true':
            return 'local_return_to_pi'
        progress_status = session.query(StudyModel.progress_status).filter(StudyModel.id == study_id).scalar()
        if progress_status:
            return progress_status.value
