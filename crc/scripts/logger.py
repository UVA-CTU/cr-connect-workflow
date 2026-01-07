"""Log to the console"""
from crc import app
from crc.api.common import ApiError
from crc.scripts.script import Script


class LoggingScript(Script):
    """Script that logs to the console"""

    def get_description(self):
        """Script that logs a message to the console.
                Requires `message`."""
        return 'Script that logs a message to the console.'

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """simple workflow validation"""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    @staticmethod
    def __build_message(study_id, workflow_id, task_id, message):
        message = \
            (f'study_id: {study_id}, '
             f'workflow_id: {workflow_id}, '
             f'task_id: {task_id}, '
             f'message: {message}')
        return message

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):
        """Log a message to the console"""
        message = ''
        if 'message' in kwargs:
            message = self.__build_message(study_id, workflow_id, task.id, kwargs['message'])
            app.logger.info(msg=message)
        elif len(args) > 0:
            message = self.__build_message(study_id, workflow_id, task.id, args[0])
            app.logger.info(msg=message)
        if message:
            app.logger.info(msg=message)
        else:
            raise ApiError(code='missing_log_message',
                           message='call to logger script missing log_message')
