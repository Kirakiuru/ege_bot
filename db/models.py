from sqlalchemy import BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)

    scores: Mapped[list["Score"]] = relationship("Score", back_populates="student", cascade="all, delete-orphan")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Score(Base):
    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject: Mapped[str] = mapped_column(String, nullable=True)
    score: Mapped[int] = mapped_column(Integer, nullable=True)
    student: Mapped["Student"] = relationship("Student", back_populates="scores")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
