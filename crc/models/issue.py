"""Model and schema for CRC support issues."""
import enum
from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from crc import db, ma

class IssueCustomer(enum.Enum):
    """Enum for customer types"""
    ctu = 'ctu'
    researcher = 'researcher'
    uva = 'uva'

class IssueType(enum.Enum):
    """Enum for issue types"""
    bug = 'bug'
    feature_request = 'feature_request'
    support = 'support'

class IssueStatus(enum.Enum):
    """Enum for issue status"""
    backlog = 'backlog'
    waiting = 'waiting'
    in_progress = 'in_progress'
    resolved = 'resolved'
    closed = 'closed'

class IssueNotesModel(db.Model):
    """Model for notes associated with issues."""
    __tablename__ = 'issue_notes'
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('UserModel', backref='issue_notes', lazy=True, foreign_keys=[author_id])

class IssueModel(db.Model):
    """Model for crc support issues."""
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    customer = db.Column(db.Enum(IssueCustomer), nullable=True)
    type = db.Column(db.Enum(IssueType), nullable=True)
    status = db.Column(db.Enum(IssueStatus), nullable=False, default=IssueStatus.backlog)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.relationship('IssueNotesModel', backref='issue', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('UserModel', backref='reported_issues', lazy=True, foreign_keys=[user_id])
    assigned_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned = db.relationship('UserModel', backref='assigned_issues', lazy=True, foreign_keys=[assigned_id])

class IssueSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = IssueModel
        sqla_session = db.session
        load_instance = True

    customer = auto_field()
    type = auto_field()
    status = auto_field()
