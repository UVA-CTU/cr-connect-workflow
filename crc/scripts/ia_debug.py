"""Template for scripts"""
from crc import session
from crc.api.common import ApiError  # noqa - this is our api error wrapper
from crc.models.workflow import WorkflowModel, WorkflowStatus
from crc.models.study import StudyModel
from crc.scripts.script import Script  # pylint disable=unable-to-import
from crc.services.protocol_builder import ProtocolBuilderService



class IADebugScript(Script):
    """Template for creating scripts"""

    pb = ProtocolBuilderService()

    def get_description(self):
        """Method that returns a description of the script."""
        return """This is my description"""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Method to validate the script."""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):  # pylint: disable=unused-argument
        """Method to perform the task."""
        irb_info = self.pb.get_irb_info(study_id)
        # workflow_ids = []
        waiting_workflows = []

        # study_status = session.query(StudyModel.status).filter(StudyModel.id == study_id).scalar()

        workflow_models = (session.query(WorkflowModel).
                         filter(WorkflowModel.study_id == study_id).
                         filter(WorkflowModel.workflow_spec_id.contains('status_check')).
                         filter(WorkflowModel.status.in_([WorkflowStatus.waiting, WorkflowStatus.erroring])).
                         all())
        ia_model = (session.query(WorkflowModel).
                    filter(WorkflowModel.workflow_spec_id == 'investigator_agreement').
                    filter(WorkflowModel.study_id==study_id).
                    first())
        investigator_agreement = {'id': 'investigator_agreement',
                                  'last_updated': ia_model.last_updated,
                                  'state': ia_model.state,
                                  'status': ia_model.status.value
                                  }
        for workflow in workflow_models:
            waiting_workflows.append({'id': workflow.id,
                                      'last_updated': workflow.last_updated,
                                      'state': workflow.state,
                                      'status': workflow.status.value,
                                      'workflow_spec_id': workflow.workflow_spec_id,
                                      })

        return (irb_info[0] if len(irb_info) > 0 else {}, waiting_workflows, investigator_agreement)
