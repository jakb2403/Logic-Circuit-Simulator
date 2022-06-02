"""Test the Names module."""
import pytest

from names import Names


@pytest.fixture
def new_names():
    """Return a new names instance."""
    return Names()


@pytest.fixture
def name_string_list():
    """Return a list of example names."""
    return ["Alice", "Bob", "Eve"]


@pytest.fixture
def unknown_name_list_ordered():
    """return a list of names, including ones that
    aren't in the names table (put at end of list)"""
    return ['Alice', 'Bob', 'Eve', 'Daniel']


@pytest.fixture
def unknown_name_list_unordered():
    """return a list of names, including ones that
    aren't in the names table (put at end of list)"""
    return ['Alice', 'Zulu', 'Bob', 'Peter', 'Eve']


# CHANGE MADE HERE! IF MESSY UNDO THIS PART!
@pytest.fixture
def used_names(name_string_list):
    """Return a names instance, after three names have been added."""
    my_name = Names()
    for name in name_string_list:
        my_name.lookup(name)
    return my_name


@pytest.fixture
def used_names_lookup1(unknown_name_list_ordered):
    """Return a names instance, after three names have been added."""
    my_name = Names()
    for name in unknown_name_list_ordered:
        my_name.lookup(name)
    return my_name


@pytest.fixture
def used_names_lookup2(unknown_name_list_unordered):
    """Return a names instance, after three names have been added."""
    my_name = Names()
    for name in unknown_name_list_unordered:
        my_name.lookup(name)
    return my_name


def test_get_string_raises_exceptions(used_names):
    """Test if get_string raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_string("hello")
    with pytest.raises(ValueError):
        used_names.get_string(-1)


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Alice"),
    (1, "Bob"),
    (2, "Eve"),
    (3, None)
])
def test_get_string(used_names, new_names, name_id, expected_string):
    """Test if get_string returns the expected string."""
    # Name is present
    assert used_names.get_string(name_id) == expected_string
    # Name is absent
    assert new_names.get_string(name_id) is None


@pytest.mark.parametrize("input_names1, expected_ids1", [
    ("Alice", 0),
    ("Bob", 1),
    ("Eve", 2),
    ("Daniel", 3)
])
def test_lookup1(used_names_lookup1, input_names1, expected_ids1):
    """Test if lookup returns the expected string"""
    # name is not present but appends to the table and returns new id
    assert used_names_lookup1.lookup(input_names1) == expected_ids1
    assert used_names_lookup1.lookup("Elisa") == 4
    pass


@pytest.mark.parametrize("input_names2, expected_ids2", [
    ("Alice", 0),
    ("Zulu", 3),
    ("Bob", 1),
    ("Peter", 4),
    ("Eve", 2)
])
def test_lookup2(used_names_lookup2, input_names2, expected_ids2):
    """Test if lookup returns the expected string"""
    assert type(input_names2) == list
    # name is not present but appends to the table and returns new id
    assert used_names_lookup2.lookup(input_names2) == expected_ids2
    assert used_names_lookup2.lookup("Elisa") == 5

    pass
