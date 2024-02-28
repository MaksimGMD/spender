from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.budget import Budget
from app.schemas.budget import BudgetSchema, BudgetCreate, BudgetUpdate
from app.api.deps import get_current_user, CurrentUser, SessionDep
from app import crud

router = APIRouter()

NOT_FOUND_MESSAGE = "Бюджет не найден"


@router.get("/{id}", response_model=BudgetSchema)
def get_budget(*, session: SessionDep, current_user: CurrentUser, id: int):
    budget = crud.budget.get(session, id)

    if not budget:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)

    if budget.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return budget


@router.get("/", response_model=List[BudgetSchema])
def get_budgets(*, session: SessionDep, current_user: CurrentUser):
    budgets = session.query(Budget).where(Budget.user_id == current_user.id).all()
    return budgets


@router.post("/", dependencies=[Depends(get_current_user)], response_model=BudgetSchema)
def create_budget(*, session: SessionDep, budget_in: BudgetCreate):
    budget = crud.budget.create(db=session, obj_in=budget_in)
    return budget


@router.put("/{budget_id}", response_model=BudgetSchema)
def update_budget(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    budget_id: int,
    budget_in: BudgetUpdate,
):
    budget = crud.budget.get(session, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if budget.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может изменить не свой бюджет"
        )

    budget = crud.budget.update(session, db_obj=budget, obj_in=budget_in)
    return budget


@router.delete("/{budget_id}")
def delete_budget(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    budget_id: int,
):
    budget = crud.budget.get(session, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MESSAGE)
    if budget.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Пользователь не может удалить не свой бюджет"
        )

    crud.goal.remove(session, id=budget_id)
    return "Бюджет удален"
