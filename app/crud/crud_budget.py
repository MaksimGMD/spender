from app.crud.base import CRUDBase
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


class CRUDBudget(CRUDBase[Budget, BudgetCreate, BudgetUpdate]):
    pass


budget = CRUDBudget(Budget)
