"""Debug Script"""
# from crc.api.common import ApiError
from crc.scripts.script import Script


class DebugScript(Script):
    """Use this when building a script task in a workflow
    Call this script if you need to debug"""

    def get_description(self):
        """Return a description of this script"""
        return """Used for debugging purposes
        not meant to be called on production code"""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Simple way to validate a task"""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):
        """code to debug"""
        # add code from the script task here
