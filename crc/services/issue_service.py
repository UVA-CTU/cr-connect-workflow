"""Service for managing issues in the system."""
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import FlushError
from typing import Optional

from crc import session
from crc.models.issue import (
    IssueModel, IssueStatus, IssueType, IssueCustomer, IssueNotesModel)  # , IssueSchema

MISSING_ISSUE_ERROR = "Issue not found"


class IssueException(Exception):
    """Custom exception for issue-related errors."""

class IssueService:
    """Service for managing issues in the system."""

    @staticmethod
    def create_issue(
            title: str,
            user_id: int,
            description: Optional[str] = None,
            customer: Optional[str] = None,
            issue_type: Optional[str] = None) -> IssueModel:
        """Create a new issue"""

        title = title.strip()
        if not title:
            raise IssueException("New issues must have a title")

        try:
            issue_model = IssueModel(
                title=title,
                user_id=user_id,
                description=description,
                customer=customer,
                type=issue_type,
                status=IssueStatus.backlog)
        except TypeError:
            raise
        except Exception as e:
            raise IssueException(f"Error creating issue: {str(e)}") from e

        try:
            session.add(issue_model)
        except FlushError:
            raise
        except SQLAlchemyError:
            raise
        except Exception as e:
            raise IssueException(f"Error adding issue to session: {str(e)}") from e

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        except SQLAlchemyError:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise IssueException(f"Error committing issue to database: {str(e)}") from e

        return issue_model

    @staticmethod
    def get_issue(issue_id: int) -> IssueModel:
        """Retrieve an issue by ID"""
        issue_model = session.query(IssueModel).filter_by(id=issue_id).first()
        if issue_model is not None and not issue_model.deleted:
            return issue_model
        raise ValueError(MISSING_ISSUE_ERROR)

    @staticmethod
    def get_issues(
            user_id: Optional[int] = None,
            deleted: Optional[bool] = False) -> list[IssueModel]:
        """Retrieve all issues, optionally filtered by user_id"""
        query = session.query(IssueModel)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if not deleted:
            query = query.filter_by(deleted=False)
        return query.all()

    def update_issue_title(self,
                     issue_id: int,
                     title: Optional[str] = None) -> IssueModel:
        """Update an existing issue"""
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        if title is not None:
            issue_model.title = title
        session.commit()
        return issue_model

    def update_issue_description(self,
                     issue_id: int,
                     description: Optional[str] = None) -> IssueModel:
        """Update an existing issue"""
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        if description is not None:
            issue_model.description = description
        session.commit()
        return issue_model

    def update_issue_status(self,
                            issue_id: int,
                            status: str) -> IssueModel:
        """Update issue status"""
        if status not in IssueStatus.__dict__.values():
            raise ValueError("Invalid status value")
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        issue_model.status = status
        session.commit()
        return issue_model

    def update_issue_type(self,
                          issue_id: int,
                          issue_type: str) -> IssueModel:
        """Update issue type"""
        if issue_type not in IssueType.__dict__.values():
            raise ValueError("Invalid issue type value")
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        issue_model.type = issue_type
        session.commit()
        return issue_model

    def update_issue_customer(self,
                              issue_id: int,
                              customer: str) -> IssueModel:
        """Update issue customer"""
        if customer not in IssueCustomer.__dict__.values():
            raise ValueError("Invalid customer value")
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        issue_model.customer = customer
        session.commit()
        return issue_model

    def delete_issue(self, issue_id: int) -> IssueModel:
        """Soft delete an existing issue"""
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        issue_model.deleted = True
        session.commit()
        return issue_model

    def add_note_to_issue(self,
                          issue_id: int,
                          note: str,
                          author: int) -> IssueNotesModel:
        """Add a note to an existing issue"""
        issue_model = self.get_issue(issue_id)
        if not issue_model:
            raise ValueError(MISSING_ISSUE_ERROR)
        note_model = IssueNotesModel(issue_id=issue_id, note=note, author=author)
        session.add(note_model)
        session.commit()
        return note_model
