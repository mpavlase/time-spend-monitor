from datetime import datetime


def test_empty_store(store):
    assert store.get_total_spent_per_project() == {}


def test_filled_store(filled_store):
    expected = {
        'one': 4 * 60,
        'two': 2 * 60,
        'three': 3 * 60,
        'four': 2 * 60,
    }
    computed = filled_store.get_total_spent_per_project(finished_at=datetime(
        2024, 1, 17, 10, 11)
    )

    assert computed == expected

def test_switch_to_same_project_does_nothing():
    ...