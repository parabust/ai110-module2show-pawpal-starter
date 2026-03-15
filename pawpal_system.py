from dataclasses import dataclass, field
from datetime import datetime
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

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks_by_owner(self, owner_id: str) -> list[Task]:
        return [t for t in self.tasks if t.owner_id == owner_id]

    def get_tasks_by_pet(self, pet_id: str) -> list[Task]:
        return [t for t in self.tasks if t.pet and t.pet.id == pet_id]

    def get_upcoming_tasks(self) -> list[Task]:
        now = datetime.now()
        return sorted(
            [t for t in self.tasks if t.scheduled_at > now],
            key=lambda t: t.scheduled_at,
        )
