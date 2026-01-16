from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MovementBase(BaseModel):
    name: str


class Movement(MovementBase):
    id: int


class EquipmentTypeBase(BaseModel):
    name: str


class EquipmentType(EquipmentTypeBase):
    id: int


class WeightliftingSetCreate(BaseModel):
    movement: str
    equipment_type: str
    n_of_reps: int
    weight: float


class WeightliftingSetUpdate(BaseModel):
    movement: str
    equipment_type: str
    n_of_reps: int
    weight: float


class WeightliftingSet(BaseModel):
    id: int
    movement: str
    equipment_type: str
    timestamp: datetime
    n_of_reps: int
    weight: float


class CardioSetCreate(BaseModel):
    movement: str
    equipment_type: str
    distance: float
    duration: float
    power_output: Optional[float] = 0


class CardioSet(BaseModel):
    id: int
    movement: str
    equipment_type: str
    timestamp: datetime
    distance: float
    duration: float
    power_output: float


class AggregatedWorkoutDay(BaseModel):
    date: str
    movement: str
    total_weight_or_reps: str
    time_elapsed: str
    sets: List[dict]


class WorkoutExerciseSummary(BaseModel):
    total_weight: float
    count: int


class WorkoutSummary(BaseModel):
    is_current: bool
    start_time: datetime
    total_minutes: int
    exercises: dict


class ImportData(BaseModel):
    movements: List[dict]
    equipmentTypes: List[dict]
    weightliftingSets: List[dict]
    cardioSets: Optional[List[dict]] = []
