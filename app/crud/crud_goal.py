from typing import Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate, GoalUpdateAmount


class CRUDGoal(CRUDBase[Goal, GoalCreate, GoalUpdate]):
    def create(self, db: Session, *, obj_in: GoalCreate):
        goal = super().create(db, obj_in=obj_in)
        new_goal = self._update_is_achieved(db, goal.id)
        return new_goal

    def update(
        self, db: Session, *, db_obj: Goal, obj_in: Union[GoalUpdate, Dict[str, Any]]
    ) -> Goal:
        goal = super().update(db, db_obj=db_obj, obj_in=obj_in)
        new_goal = self._update_is_achieved(db, goal.id)
        return new_goal

    def _update_is_achieved(self, db: Session, goal_id: int) -> Goal:
        goal = self.get(db, goal_id)
        if goal:
            goal.is_achieved = goal.amount >= goal.target_amount
            db.commit()
            db.refresh(goal)
        return goal

    def add_accumulated_amount(
        self, db: Session, db_obj: Goal, obj_in: GoalUpdateAmount, goal_id: int
    ):
        """
        Добавляет или вычитает новую сумму из текущей суммы цели.
        """
        db_obj.amount += obj_in.amount
        db.commit()
        db.refresh(db_obj)
        goal = self._update_is_achieved(db, goal_id)
        return goal


goal = CRUDGoal(Goal)
