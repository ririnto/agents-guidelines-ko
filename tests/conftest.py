import pytest


@pytest.fixture
def mock_repo_dir(tmp_path):
    return tmp_path / "fake_repo"


@pytest.fixture
def mock_logger():
    import logging

    return logging.getLogger("test_logger")
