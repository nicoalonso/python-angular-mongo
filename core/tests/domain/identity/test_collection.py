import pytest

from src.domain.identity.collection import Collection

class TestCollection:
    def test_should_create_an_empty_collection(self):
        collection = Collection()

        assert collection.to_array() == []
        assert len(collection) == 0
        assert collection.count() == 0
        assert collection.is_empty() is True
        assert bool(collection) is False

        assert collection[0:10] == []
        pytest.raises(IndexError, collection.__getitem__, 0)
        assert collection.first() is None
        assert collection.last() is None
        assert collection.get(0) is None
        assert collection.index_of(0) == -1
        assert collection.remove(0) is False

        assert collection.filter(lambda x: True).count() == 0
        assert collection.find_first(lambda x: True) is None

    def test_should_run_when_create_collection_of_ints(self):
        collection = Collection([1, 2, 3])

        assert collection.to_array() == [1, 2, 3]
        assert len(collection) == 3
        assert collection.count() == 3
        assert collection.is_empty() is False
        assert bool(collection) is True

        assert collection[0] == 1
        assert collection[1] == 2
        assert collection[2] == 3
        pytest.raises(IndexError, collection.__getitem__, 3)

        assert collection.first() == 1
        assert collection.last() == 3
        assert collection.get(1) == 2
        assert collection.index_of(2) == 1

        assert collection.filter(lambda x: x > 1).to_array() == [2, 3]
        assert collection.find_first(lambda x: x > 1) == 2

        assert collection.remove(2) is True
        assert collection.to_array() == [1, 3]

    def test_should_run_when_create_collection_of_strings(self):
        collection = Collection(['a', 'b', 'c'])

        assert collection.to_array() == ['a', 'b', 'c']
        assert len(collection) == 3
        assert collection.count() == 3
        assert collection.is_empty() is False

        assert collection[0] == 'a'
        assert collection[1] == 'b'
        assert collection[2] == 'c'
        pytest.raises(IndexError, collection.__getitem__, 3)

        assert collection.first() == 'a'
        assert collection.last() == 'c'
        assert collection.get(1) == 'b'
        assert collection.index_of('b') == 1

        assert collection.filter(lambda x: x > 'a').to_array() == ['b', 'c']
        assert collection.find_first(lambda x: x > 'a') == 'b'

        assert collection.remove('b') is True
        assert collection.to_array() == ['a', 'c']

    def test_should_run_when_add_elements_to_collection(self):
        collection = Collection()

        collection.add(1)
        collection.add(2)
        collection.add(3)

        assert collection.to_array() == [1, 2, 3]
        assert len(collection) == 3
        assert collection.count() == 3

    def test_should_run_when_replace_an_element(self):
        collection = Collection([1, 2, 3])

        collection.set(1, 4)

        assert collection.to_array() == [1, 4, 3]
        assert len(collection) == 3
        assert collection.count() == 3

    def test_should_fail_when_replace_an_element_with_invalid_index(self):
        collection = Collection([1, 2, 3])

        collection.set(-1, 4)
        collection.set(3, 4)

        assert collection.to_array() == [1, 2, 3]

    def test_should_run_when_remove_an_element(self):
        collection = Collection([1, 2, 3])

        assert collection.remove(2) is True
        assert collection.to_array() == [1, 3]

    def test_should_run_when_clear(self):
        collection = Collection([1, 2, 3])

        collection.clear()

        assert collection.to_array() == []
        assert len(collection) == 0
        assert collection.count() == 0
        assert collection.is_empty() is True

    def test_should_run_when_map(self):
        collection = Collection([1, 2, 3])

        mapped = collection.map(lambda x: x * 2)

        assert mapped.to_array() == [2, 4, 6]
        assert len(mapped) == 3
        assert mapped.count() == 3

    def test_should_run_when_filter(self):
        collection = Collection([1, 2, 3])

        filtered = collection.filter(lambda x: x > 1)

        assert filtered.to_array() == [2, 3]
        assert len(filtered) == 2
        assert filtered.count() == 2

    def test_should_run_when_find_first(self):
        collection = Collection([1, 2, 3])

        assert collection.find_first(lambda x: x > 1) == 2
        assert collection.find_first(lambda x: x > 3) is None

    def test_should_run_when_exists(self):
        collection = Collection([1, 2, 3])

        assert collection.exists(lambda x: x > 1) is True
        assert collection.exists(lambda x: x > 3) is False

    def test_should_run_when_index_of(self):
        collection = Collection([1, 2, 3])

        assert collection.index_of(2) == 1
        assert collection.index_of(4) == -1

    def test_should_run_when_iterate(self):
        collection = Collection([1, 2, 3])

        items = []
        for item in collection:
            items.append(item)

        assert items == [1, 2, 3]

    def test_should_run_when_check_if_contains(self):
        collection = Collection([1, 2, 3])

        assert 2 in collection
        assert 4 not in collection
