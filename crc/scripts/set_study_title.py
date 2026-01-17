"""Set the study title"""
from crc import session
from crc.api.common import ApiError # noqa - this is our api error wrapper
from crc.models.study import StudySchema, StudyModel
from crc.scripts.script import Script # pylint disable=unable-to-import


class SetStudyTitle(Script):
    """Set the study title"""

    def get_description(self):
        """Script that sets the study title."""
        return """Script that sets the study title.
        Note that this can be overridden by Protocol Builder."""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Method to validate the script."""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):  # pylint: disable=unused-argument
        """Method to perform the task."""
        new_title = kwargs.get('new_title', None)
        if new_title:
            study_model = session.query(StudyModel).filter(StudyModel.id == study_id).first()
            if study_model:
                study_model.title = new_title
                session.commit()
                return study_model.title

        raise ApiError(code='missing_parameter',
                       message='The set_study_title script requires a `new_title` parameter')
