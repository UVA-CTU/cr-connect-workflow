"""Test the set_study_title script."""
from unittest.mock import patch
from tests.base_test import BaseTest  # has to be imported before crc
from crc import connexion_app, session


class TestSetStudyTitle(BaseTest):
    """Test the set_study_title script."""

    def test_set_study_title(self):
        """Test the set_study_title script."""
        workflow = self.create_workflow('set_study_title')
        # check original title
        current_study_title = workflow.study.title
        assert current_study_title == 'Beer consumption in the bipedal software engineer'

        # complete the form
        # this calls the set_study_title script
        workflow_api = self.get_workflow_api(workflow)
        task = workflow_api.next_task
        workflow_api = self.complete_form(workflow, task, {'new_title': 'This is a new title'})

        task = workflow_api.next_task
        # if the set_study_title succeeds it returns the new title
        assert task.data['result'] == 'This is a new title'
