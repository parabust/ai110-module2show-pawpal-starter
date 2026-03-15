from datetime import datetime
from pawpal_system import Pet, Owner, Scheduler

# Create owner
owner = Owner(id="owner-1", name="Alex Rivera", email="alex@example.com")

# Create two pets
buddy = Pet(id="pet-1", name="Buddy", species="Dog", breed="Golden Retriever", age=3)
whiskers = Pet(id="pet-2", name="Whiskers", species="Cat", breed="Tabby", age=5)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# Create tasks
morning_walk = owner.create_task(buddy, "Walk", datetime(2026, 3, 15, 8, 0))
morning_walk.description = "30-minute morning walk around the park"

feeding = owner.create_task(whiskers, "Feed", datetime(2026, 3, 15, 9, 30))
feeding.description = "Morning feeding - half cup of dry food"

vet_checkup = owner.create_task(buddy, "Vet Appointment", datetime(2026, 3, 15, 14, 0))
vet_checkup.description = "Annual checkup and vaccinations"

grooming = owner.create_task(whiskers, "Grooming", datetime(2026, 3, 15, 16, 30))
grooming.description = "Brush coat and trim nails"

# Intentional conflict: same time as evening_walk to trigger a warning
playtime = owner.create_task(whiskers, "Playtime", datetime(2026, 3, 15, 18, 0))
playtime.description = "Indoor play session with feather toy"

evening_walk = owner.create_task(buddy, "Walk", datetime(2026, 3, 15, 18, 0))
evening_walk.description = "Evening walk around the neighborhood"

# Register tasks with scheduler
scheduler = Scheduler(id="scheduler-1")
for task in owner.tasks:
    scheduler.add_task(task)

# Print today's schedule
print("=" * 45)
print(f"  PawPal+ Schedule for {datetime(2026, 3, 15).strftime('%B %d, %Y')}")
print(f"  Owner: {owner.name}")
print("=" * 45)

today_tasks = sorted(owner.tasks, key=lambda t: t.scheduled_at)
for task in today_tasks:
    time_str = task.scheduled_at.strftime("%I:%M %p")
    print(f"\n  {time_str} — {task.action} ({task.pet.name})")
    print(f"  {task.description}")
    print(f"  Status: {task.status}")

print("\n" + "=" * 45)
print(f"  Total tasks today: {len(today_tasks)}")
print("=" * 45)
