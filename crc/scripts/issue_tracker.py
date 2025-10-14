"""Script to manage crc support issues"""
from crc.api.common import ApiError
from crc.scripts.script import Script
from crc.services.issue_service import IssueService
from crc.models.user import UserModel
from crc.models.issue import IssueSchema


class IssueTracker(Script):
    """Simple interface to manage crc support issues"""

    def get_description(self):
        """Returns a description of this script"""
        return """This is my description"""

    def do_task_validate_only(self, task, study_id, workflow_id, *args, **kwargs):
        """Allows simple validation of script syntax"""
        return self.do_task(task, study_id, workflow_id, *args, **kwargs)

    @staticmethod
    def create_issue(title, user_id, description):
        """Create a new issue"""
        issue_service = IssueService()
        issue = issue_service.create_issue(title=title, user_id=user_id, description=description)
        return issue

    @staticmethod
    def get_issue(issue_id):
        """Get an issue by ID"""
        issue_service = IssueService()
        issue = issue_service.get_issue(issue_id=issue_id)
        return issue

    @staticmethod
    def update_issue(issue_id, title=None, description=None):
        """Update an existing issue"""
        issue_service = IssueService()
        issue = issue_service.update_issue(issue_id=issue_id, title=title, description=description)
        return issue

    @staticmethod
    def update_issue_status(issue_id, status):
        """Update issue status"""
        issue_service = IssueService()
        issue = issue_service.update_issue_status(issue_id=issue_id, status=status)
        return issue

    @staticmethod
    def update_issue_type(issue_id, issue_type):
        """Update issue type"""
        issue_service = IssueService()
        issue = issue_service.update_issue_type(issue_id=issue_id, issue_type=issue_type)
        return issue

    @staticmethod
    def update_issue_customer(issue_id, customer):
        """Update issue customer"""
        issue_service = IssueService()
        issue = issue_service.update_issue_customer(issue_id=issue_id, customer=customer)
        return issue

    @staticmethod
    def delete_issue(issue_id):
        """Soft delete an existing issue"""
        issue_service = IssueService()
        issue = issue_service.delete_issue(issue_id=issue_id)
        return issue

    def get_issues(self, user_id=None, deleted_issues=False):
        """Get all issues, optionally filtered by user_id and deleted status"""
        issue_service = IssueService()
        issues = issue_service.get_issues(user_id=user_id, deleted=deleted_issues)
        return issues

    def do_task(self, task, study_id, workflow_id, *args, **kwargs):
        """Main method to perform the script's task"""
        action = kwargs.get('action', None)
        if not action:
            raise ApiError(code='missing_parameters',
                           message='The issue_tracker script requires an action parameter.')

        issue_id = kwargs.get('issue_id', None)
        title = kwargs.get('title', None)
        description = kwargs.get('description', None)
        customer = kwargs.get('customer', None)
        issue_type = kwargs.get('issue_type', None)
        status = kwargs.get('status', None)
        deleted_issues = kwargs.get('deleted_issues', False)
        current_user = task.data['get_current_user']()['uid']
        current_user_id = UserModel.query.filter_by(uid=current_user).first().id

        if action == 'create':
            if not title or not current_user_id:
                raise ApiError(
                    code='missing_parameters',
                    message='Creating an issue requires title and description parameters.')
            issue_model = self.create_issue(title, current_user_id, description)
            return IssueSchema().dump(issue_model)


        elif action == 'update':
            if not issue_id:
                raise ApiError(code='missing_parameters',
                               message='Updating an issue requires issue_id parameter.')
            issue_service = IssueService()
            issue = issue_service.get_issue(issue_id)
            if not issue:
                raise ApiError(code='missing_issue',
                               message='No issue found with the provided issue_id.')
            return self.update_issue(issue_id, title, description)

        elif action == 'update_status':
            if not issue_id or not status:
                raise ApiError(
                    code='missing_parameters',
                    message='Updating issue status requires issue_id and status parameters.')
            return self.update_issue_status(issue_id, status)

        elif action == 'update_type':
            if not issue_id or not issue_type:
                raise ApiError(
                    code='missing_parameters',
                    message='Updating issue type requires issue_id and issue_type parameters.')
            return self.update_issue_type(issue_id, issue_type)

        elif action == 'update_customer':
            if not issue_id or not customer:
                raise ApiError(
                    code='missing_parameters',
                    message='Updating issue customer requires issue_id and customer parameters.')
            return self.update_issue_customer(issue_id, customer)

        elif action == 'delete':
            if not issue_id:
                raise ApiError(code='missing_parameters',
                               message='Deleting an issue requires issue_id parameter.')
            return self.delete_issue(issue_id)

        elif action == 'issue':
            if not issue_id:
                raise ApiError(code='missing_parameters',
                               message='Retrieving an issue requires issue_id parameter.')
            issue_model = self.get_issue(issue_id)
            return IssueSchema().dump(issue_model)

        elif action == 'issues':
            if not current_user_id:
                raise ApiError(code='missing_parameters',
                               message='Retrieving issues requires current_user_id parameter.')
            issues = self.get_issues(user_id=current_user_id, deleted_issues=deleted_issues)
            return IssueSchema().dump(issues, many=True)

        raise ApiError(code='invalid_action',
                       message='The action parameter must be: create, update, update_status, '
                               'update_type, update_customer, delete, issue, issues.')
