from parse import Parser

@pytest.fixture
def new_parser():
    """Return a new parser instance."""
    return Parser()

