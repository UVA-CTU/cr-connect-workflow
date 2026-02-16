"""Local process for returning a study to the PI.
The IRB is not able to use the existing process using the API.
This is a workaround.
This does not break the existing process using the API.
The existing process will work if the IRB uses it in the future"""

from crc.api.common import ApiError
from crc.scripts.script import Script # pylint disable=unable-to-import


class LocalReturnToPI(Script):
    """Local process for returning a study to the PI."""

    def get_description(self):
        """Local process for returning a study to the PI."""
        return """Local process for returning a study to the PI."""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Method to validate the script."""
        result = self.do_task(task, study_id, workflow_id, *args, **kwargs)
        return result

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):  # pylint: disable=unused-argument
        """Method to perform the task."""
        if 'mode' in kwargs:
            mode = kwargs['mode']
            if mode == 'get_current':
                sds_local_return_to_pi = task.data['data_store_get'](
                    type='study',
                    key='sds_local_return_to_pi')
                return {'sds_local_return_to_pi': sds_local_return_to_pi}
            if mode == 'turn_resubmission_on':
                sds_local_return_to_pi = True
                task.data['data_store_set'](type='study', key='sds_local_return_to_pi',
                                            value=sds_local_return_to_pi)
                return {'message': 'Toggle Resubmission is turned on'}

            task.data['data_store_set'](type='study', key='sds_local_return_to_pi',value='')
            return {'message': 'Toggle Resubmission is turned off'}

        raise ApiError(code='missing_parameter', message="mode not provided")
