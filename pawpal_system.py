from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import uuid


@dataclass
class Pet:
    id: str
    name: str
    species: str
    breed: str
    age: int


@dataclass
class Task:
    id: str
    action: str
    description: str
    status: str
    scheduled_at: datetime
    created_at: datetime
    pet: Optional["Pet"] = None
    owner_id: Optional[str] = None
    recurrence: Optional[str] = None  # "daily", "weekly", or None


class Owner:
    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        self.pets = [p for p in self.pets if p.id != pet_id]

    def create_task(self, pet: Pet, action: str, scheduled_at: datetime) -> Task:
        task = Task(
            id=str(uuid.uuid4()),
            action=action,
            description="",
            status="pending",
            scheduled_at=scheduled_at,
            created_at=datetime.now(),
            pet=pet,
            owner_id=self.id,
        )
        self.tasks.append(task)
        return task


class Scheduler:
    def __init__(self, id: str):
        self.id = id
        self.tasks: list[Task] = []

    def _get_conflicts(self, task: Task) -> list[Task]:
        return [
            t for t in self.tasks
            if t.scheduled_at == task.scheduled_at and t.id != task.id
        ]

    def add_task(self, task: Task) -> None:
        conflicts = self._get_conflicts(task)
        for conflict in conflicts:
            pet_label = f"{task.pet.name}" if task.pet else "Unknown pet"
            conflict_label = f"{conflict.pet.name}" if conflict.pet else "Unknown pet"
            print(
                f"Warning: '{task.action}' for {pet_label} conflicts with "
                f"'{conflict.action}' for {conflict_label} at "
                f"{task.scheduled_at.strftime('%b %d, %I:%M %p')}."
            )
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks_by_owner(self, owner_id: str) -> list[Task]:
        return [t for t in self.tasks if t.owner_id == owner_id]

    def get_tasks_by_pet(self, pet_id: str) -> list[Task]:
        return [t for t in self.tasks if t.pet and t.pet.id == pet_id]

    def filter_tasks(
        self,
        status: Optional[str] = None,
        pet_name: Optional[str] = None,
    ) -> list[Task]:
        result = self.tasks
        if status is not None:
            result = [t for t in result if t.status == status]
        if pet_name is not None:
            result = [t for t in result if t.pet and t.pet.name == pet_name]
        return result

    def mark_complete(self, task_id: str) -> Optional[Task]:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task is None:
            return None

        task.status = "completed"

        if task.recurrence == "daily":
            delta = timedelta(days=1)
        elif task.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        next_task = Task(
            id=str(uuid.uuid4()),
            action=task.action,
            description=task.description,
            status="pending",
            scheduled_at=task.scheduled_at + delta,
            created_at=datetime.now(),
            pet=task.pet,
            owner_id=task.owner_id,
            recurrence=task.recurrence,
        )
        self.tasks.append(next_task)
        return next_task

    def sort_by_time(self) -> list[Task]:
        return sorted(self.tasks, key=lambda t: t.scheduled_at)

    def get_upcoming_tasks(self) -> list[Task]:
        now = datetime.now()
        return sorted(
            [t for t in self.tasks if t.scheduled_at > now],
            key=lambda t: t.scheduled_at,
        )
