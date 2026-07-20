from crc import session
from crc.api.common import ApiError
from crc.models.study import ProgressStatus, StudyModel
from crc.models.workflow import WorkflowModel, WorkflowStatus


def set_workflow_status(workflow_id, body):
    new_workflow_status = body['new_workflow_status']
    try:
        workflow_status = WorkflowStatus(new_workflow_status)
    except ValueError:
        raise ApiError('invalid_status', f'{new_workflow_status} is not a valid WorkflowStatus')

    workflow_model = WorkflowModel.query.filter(WorkflowModel.id == workflow_id).first()
    if not workflow_model:
        raise ApiError('workflow_not_found', f'No workflow found with id {workflow_id}')

    workflow_model.status = workflow_status
    session.commit()
    return {'status': workflow_model.status.value}


def set_study_progress_status(study_id, body):
    new_status = body['new_status']
    try:
        progress_status = ProgressStatus[new_status]
    except KeyError:
        raise ApiError('invalid_status', f'{new_status} is not a valid ProgressStatus')

    study_model = StudyModel.query.filter(StudyModel.id == study_id).first()
    if not study_model:
        raise ApiError('study_not_found', f'No study found with id {study_id}')

    study_model.progress_status = progress_status
    session.commit()
    return {'progress_status': study_model.progress_status.value}