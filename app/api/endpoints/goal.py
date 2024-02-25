from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app.models.goal import Goal
from app.schemas.goal import GoalSchema, GoalCreate, GoalUpdate, GoalUpdateAmount
from app.api.deps import get_current_user, get_session, CurrentUser
from app import crud

NOT_FOUND_MESSAGE = "Цель не найдена"

router = APIRouter()


@router.get("/", response_model=List[GoalSchema])
def get_goals(*, session: Session = Depends(get_session), current_user: CurrentUser):
    """
    **Получает список категорий для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.

    Returns:
        List[GoalSchema]: Список целей пользователя.
    """
    goals = session.exec(select(Goal).where(Goal.user_id == current_user.id)).all()
    return goals


@router.post("/", dependencies=[Depends(get_current_user)], response_model=GoalSchema)
def create_goal(*, session: Session = Depends(get_session), goal_in: GoalCreate):
    """
    **Создает новую цель для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        goal_in (GoalCreate): Данные для создания новой цели.

    Returns:
        GoalSchema: Созданная цель.
    """
    goal = crud.goal.create(db=session, obj_in=goal_in)
    return goal


@router.put("/{goal_id}", response_model=GoalSchema)
def update_goal(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUser,
    goal_id: int,
    goal_in: GoalUpdate,
):
    """
    **Обновляет существующую цель для текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        goal_id (int): Идентификатор обновляемой цели.
        goal_in (GoalUpdate): Данные для обновления цели.

    Returns:
        GoalSchema: Обновленная цель.

    Raises:
        HTTPException: Если цель не найдена или пользователь пытается изменить чужую цель.
    """
    goal = crud.goal.get(session, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может изменить не свою цель"
        )

    goal = crud.goal.update(session, db_obj=goal, obj_in=goal_in)
    return goal


@router.put("/add_accumulated_amount/{goal_id}", response_model=GoalSchema)
def add_accumulated_amount(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUser,
    goal_id: int,
    goal_in: GoalUpdateAmount,
):
    """
    **Добавляет накопленную сумму к текущей сумме цели.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        goal_id (int): Идентификатор цели, к которой добавляется сумма.
        goal_in (GoalUpdateAmount): Данные для добавления суммы.

    Returns:
        GoalSchema: Обновленная цель.

    Raises:
        HTTPException: Если цель не найдена или пользователь пытается изменить чужую цель.
    """
    goal = crud.goal.get(session, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может изменить не свою цель"
        )

    goal = crud.goal.add_accumulated_amount(
        session, db_obj=goal, obj_in=goal_in, goal_id=goal_id
    )
    return goal


@router.delete("/{goal_id}")
def delete_goal(
    *,
    session: Session = Depends(get_session),
    current_user: CurrentUser,
    goal_id: int,
):
    """
    **Удаляет цель текущего пользователя.**

    Args:
        session (Session, optional): Сессия базы данных. Defaults to Depends(get_session).
        current_user (CurrentUser): Текущий авторизованный пользователь.
        goal_id (int): Идентификатор удаляемой цели.

    Returns:
        str: Сообщение об удалении цели.

    Raises:
        HTTPException: Если цель не найдена или пользователь пытается удалить чужую цель.
    """
    goal = crud.goal.get(session, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if goal.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может удалить не свою цель"
        )

    crud.goal.remove(session, id=goal_id)
    return f"Цель: {goal.name} удалена"
