from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from .base import connection
from .models import Student, Score
from config import logger


@connection
async def set_student(session, tg_id: int, first_name: str,
                      last_name: str) -> Optional[Student]:
    try:
        student = await session.scalar(select(Student).filter_by(id=tg_id))

        if not student:
            new_student = Student(
                id=tg_id, first_name=first_name,
                last_name=last_name)
            session.add(new_student)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return student
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()


@connection
async def add_score(session, tg_id: int, subject: str,
                    score: int) -> Optional[Score]:
    try:
        student = await session.scalar(select(Student).filter_by(id=tg_id))
        if not student:
            logger.error(f"Пользователь с ID {tg_id} не найден.")
            return None
        else:
            new_score = Score(
                student_id=tg_id,
                subject=subject,
                score=score
            )
            session.add(new_score)
            await session.commit()
            logger.info(
                f"Результат для пользователя с ID {tg_id} успешно добавлен!"
                )
            return new_score
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении результата: {e}")
        await session.rollback()


@connection
async def login_user(session, tg_id: int) -> Optional[Student]:
    try:
        student = await session.scalar(select(Student).filter_by(id=tg_id))
        if not student:
            logger.info(f"Пользователь с ID {tg_id} не найден!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return student

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении результата: {e}")
        await session.rollback()


@connection
async def view_score(session, tg_id: int) -> List[Dict[str, int]]:
    try:
        score = await session.execute(
            select(Score).filter_by(student_id=tg_id)
            )
        scores = score.scalars().all()
        if not scores:
            logger.info(f"Результаты пользователя с ID {tg_id} не найдены!")
            return []
        else:
            score_list = [
                {
                    'subject': score.subject,
                    'score': score.score
                } for score in scores
            ]
            return score_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении результатов: {e}")
        return []
