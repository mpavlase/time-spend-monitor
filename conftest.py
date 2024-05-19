import pytest
from localstore import LocalStore
from datetime import datetime

@pytest.fixture
def store():
    instance = LocalStore()
    return instance


@pytest.fixture
def filled_store(store: LocalStore):
    date = 2024, 1, 17
    store.switch_to('one', datetime(*date, 10, 0))
    store.switch_to('three', datetime(*date, 10, 1))
    store.switch_to('one', datetime(*date, 10, 2))
    store.switch_to('four', datetime(*date, 10, 3))
    store.switch_to('two', datetime(*date, 10, 4))
    store.switch_to('one', datetime(*date, 10, 5))
    store.switch_to('two', datetime(*date, 10, 6))
    store.switch_to('three', datetime(*date, 10, 7))
    store.switch_to('four', datetime(*date, 10, 8))
    store.switch_to('three', datetime(*date, 10, 9))
    store.switch_to('one', datetime(*date, 10, 10))

    return store
