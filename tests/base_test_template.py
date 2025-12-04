"""Template for creating new tests."""
from unittest.mock import patch
from tests.base_test import BaseTest  # has to be imported before crc
from crc import connexion_app, session


class TestTemplate(BaseTest):
    """Template for creating new tests."""

    def test_template(self):
        """Template for creating new tests."""
        workflow = self.create_workflow('hello_world')
        workflow_api = self.get_workflow_api(workflow)
        task = workflow_api.next_task
        # make some assertion
        assert task
