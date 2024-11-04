from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()

class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = mapped_column(Integer, primary_key=True)
    password = mapped_column(String(128), nullable=False)
    is_superuser = mapped_column(Boolean, nullable=False)
    username = mapped_column(String(150), nullable=False)
    last_name = mapped_column(String(150), nullable=False)
    email = mapped_column(String(254), nullable=False)
    is_staff = mapped_column(Boolean, nullable=False)
    is_active = mapped_column(Boolean, nullable=False)
    date_joined = mapped_column(DateTime, nullable=False)
    first_name = mapped_column(String(150), nullable=False)
    last_login = mapped_column(DateTime)

    users_userprofile: Mapped[List['UsersUserprofile']] = relationship('UsersUserprofile', uselist=True, back_populates='user')

class BaseResearchwork(Base):
    __tablename__ = 'base_researchwork'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=False)

    base_topic: Mapped[List['BaseTopic']] = relationship('BaseTopic', uselist=True, back_populates='research_work')
    base_submission: Mapped[List['BaseSubmission']] = relationship('BaseSubmission', uselist=True, back_populates='research_work')


class UsersGroup(Base):
    __tablename__ = 'users_group'

    id = mapped_column(Integer, primary_key=True)
    group_name = mapped_column(String(20), nullable=False)

    users_userprofile: Mapped[List['UsersUserprofile']] = relationship('UsersUserprofile', uselist=True, back_populates='group')

class BaseTopic(Base):
    __tablename__ = 'base_topic'
    __table_args__ = (
        Index('base_topic_research_work_id_f512bc53', 'research_work_id'),
    )

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    research_work_id = mapped_column(ForeignKey('base_researchwork.id'))

    research_work: Mapped[Optional['BaseResearchwork']] = relationship('BaseResearchwork', back_populates='base_topic')
    base_file: Mapped[List['BaseFile']] = relationship('BaseFile', uselist=True, back_populates='topic')


class UsersUserprofile(Base):
    __tablename__ = 'users_userprofile'
    __table_args__ = (
        Index('users_userprofile_group_id_d32cb94c', 'group_id'),
    )

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey('auth_user.id'), nullable=False)
    group_id = mapped_column(ForeignKey('users_group.id'))
    middle_name = mapped_column(String(30))
    role = mapped_column(String(20))

    group: Mapped[Optional['UsersGroup']] = relationship('UsersGroup', back_populates='users_userprofile')
    user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='users_userprofile')
    base_assignment: Mapped[List['BaseAssignment']] = relationship('BaseAssignment', uselist=True, foreign_keys='[BaseAssignment.student_id]', back_populates='student')
    base_assignment_: Mapped[List['BaseAssignment']] = relationship('BaseAssignment', uselist=True, foreign_keys='[BaseAssignment.teacher_id]', back_populates='teacher')

class BaseAssignment(Base):
    __tablename__ = 'base_assignment'
    __table_args__ = (
        Index('base_assignment_student_id_28cc3722', 'student_id'),
        Index('base_assignment_teacher_id_829fa074', 'teacher_id')
    )

    id = mapped_column(Integer, primary_key=True)
    is_accepted = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    student_id = mapped_column(ForeignKey('users_userprofile.id'), nullable=False)
    teacher_id = mapped_column(ForeignKey('users_userprofile.id'), nullable=False)
    text = mapped_column(Text, nullable=False)
    is_reviewed = mapped_column(Boolean, nullable=False)

    student: Mapped['UsersUserprofile'] = relationship('UsersUserprofile', foreign_keys=[student_id], back_populates='base_assignment')
    teacher: Mapped['UsersUserprofile'] = relationship('UsersUserprofile', foreign_keys=[teacher_id], back_populates='base_assignment_')
    base_submission: Mapped[List['BaseSubmission']] = relationship('BaseSubmission', uselist=True, back_populates='assignment')


class BaseSubmission(Base):
    __tablename__ = 'base_submission'
    __table_args__ = (
        Index('base_submission_assignment_id_907d9d53', 'assignment_id'),
        Index('base_submission_research_work_id_6a4c7968', 'research_work_id')
    )

    id = mapped_column(Integer, primary_key=True)
    assignment_id = mapped_column(ForeignKey('base_assignment.id'), nullable=False)
    semester = mapped_column(String(100))
    created_at = mapped_column(DateTime)
    research_work_id = mapped_column(ForeignKey('base_researchwork.id'))

    assignment: Mapped['BaseAssignment'] = relationship('BaseAssignment', back_populates='base_submission')
    research_work: Mapped[Optional['BaseResearchwork']] = relationship('BaseResearchwork', back_populates='base_submission')
    base_file: Mapped[List['BaseFile']] = relationship('BaseFile', uselist=True, back_populates='submission')


class BaseFile(Base):
    __tablename__ = 'base_file'
    __table_args__ = (
        Index('base_file_submission_id_a4445a9e', 'submission_id'),
        Index('base_file_topic_id_0936a51b', 'topic_id')
    )

    id = mapped_column(Integer, primary_key=True)
    is_accepted = mapped_column(Boolean, nullable=False)
    upload_date = mapped_column(DateTime, nullable=False)
    is_reviewed = mapped_column(Boolean, nullable=False)
    filename = mapped_column(String(100))
    topic_id = mapped_column(ForeignKey('base_topic.id'))
    submission_id = mapped_column(ForeignKey('base_submission.id'))
    comment = mapped_column(Text)

    submission: Mapped[Optional['BaseSubmission']] = relationship('BaseSubmission', back_populates='base_file')
    topic: Mapped[Optional['BaseTopic']] = relationship('BaseTopic', back_populates='base_file')
