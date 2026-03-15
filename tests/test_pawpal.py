import pytest
from datetime import datetime
from pawpal_system import Pet, Task, Owner, Scheduler


# --- Fixtures ---

@pytest.fixture
def pet():
    return Pet(id="pet-1", name="Buddy", species="Dog", breed="Golden Retriever", age=3)

@pytest.fixture
def second_pet():
    return Pet(id="pet-2", name="Whiskers", species="Cat", breed="Tabby", age=5)

@pytest.fixture
def owner():
    return Owner(id="owner-1", name="Alex Rivera", email="alex@example.com")

@pytest.fixture
def scheduler():
    return Scheduler(id="scheduler-1")

@pytest.fixture
def future_time():
    return datetime(2099, 1, 1, 10, 0)


# --- Pet ---

def test_pet_attributes(pet):
    assert pet.id == "pet-1"
    assert pet.name == "Buddy"
    assert pet.species == "Dog"
    assert pet.breed == "Golden Retriever"
    assert pet.age == 3


# --- Owner ---

def test_owner_attributes(owner):
    assert owner.id == "owner-1"
    assert owner.name == "Alex Rivera"
    assert owner.email == "alex@example.com"
    assert owner.pets == []
    assert owner.tasks == []

def test_add_pet(owner, pet):
    owner.add_pet(pet)
    assert pet in owner.pets

def test_add_multiple_pets(owner, pet, second_pet):
    owner.add_pet(pet)
    owner.add_pet(second_pet)
    assert len(owner.pets) == 2

def test_remove_pet(owner, pet):
    owner.add_pet(pet)
    owner.remove_pet(pet.id)
    assert pet not in owner.pets

def test_remove_pet_nonexistent(owner):
    owner.remove_pet("does-not-exist")
    assert owner.pets == []

def test_create_task_returns_task(owner, pet, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    assert isinstance(task, Task)

def test_create_task_fields(owner, pet, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    assert task.action == "Walk"
    assert task.pet == pet
    assert task.owner_id == owner.id
    assert task.scheduled_at == future_time
    assert task.status == "pending"

def test_create_task_has_id(owner, pet, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    assert task.id is not None
    assert len(task.id) > 0

def test_create_task_unique_ids(owner, pet, future_time):
    task1 = owner.create_task(pet, "Walk", future_time)
    task2 = owner.create_task(pet, "Feed", future_time)
    assert task1.id != task2.id

def test_create_task_added_to_owner(owner, pet, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    assert task in owner.tasks


# --- Scheduler ---

def test_add_task(owner, pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    assert task in scheduler.tasks

def test_remove_task(owner, pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    scheduler.remove_task(task.id)
    assert task not in scheduler.tasks

def test_remove_task_nonexistent(scheduler):
    scheduler.remove_task("does-not-exist")
    assert scheduler.tasks == []

def test_get_tasks_by_owner(owner, pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    result = scheduler.get_tasks_by_owner(owner.id)
    assert task in result

def test_get_tasks_by_owner_filters_correctly(owner, pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    result = scheduler.get_tasks_by_owner("other-owner-id")
    assert task not in result

def test_get_tasks_by_pet(owner, pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    result = scheduler.get_tasks_by_pet(pet.id)
    assert task in result

def test_get_tasks_by_pet_filters_correctly(owner, pet, second_pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    result = scheduler.get_tasks_by_pet(second_pet.id)
    assert task not in result

def test_get_upcoming_tasks(owner, pet, scheduler, future_time):
    task = owner.create_task(pet, "Walk", future_time)
    scheduler.add_task(task)
    result = scheduler.get_upcoming_tasks()
    assert task in result

def test_get_upcoming_tasks_excludes_past(owner, pet, scheduler):
    past_task = owner.create_task(pet, "Walk", datetime(2000, 1, 1, 8, 0))
    scheduler.add_task(past_task)
    result = scheduler.get_upcoming_tasks()
    assert past_task not in result

def test_get_upcoming_tasks_sorted(owner, pet, scheduler):
    task1 = owner.create_task(pet, "Walk", datetime(2099, 6, 1, 18, 0))
    task2 = owner.create_task(pet, "Feed", datetime(2099, 6, 1, 9, 0))
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    result = scheduler.get_upcoming_tasks()
    assert result[0].scheduled_at < result[1].scheduled_at
