from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from nir_myrmiaka.db.base import Base

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

    group = relationship('UsersGroup', back_populates='users_userprofile')
    user = relationship('AuthUser', back_populates='users_userprofile')
    base_assignment = relationship('BaseAssignment', uselist=True, foreign_keys='[BaseAssignment.student_id]', back_populates='student')
    base_assignment_ = relationship('BaseAssignment', uselist=True, foreign_keys='[BaseAssignment.teacher_id]', back_populates='teacher')
