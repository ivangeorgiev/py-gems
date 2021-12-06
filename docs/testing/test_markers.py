import pytest

pytestmark = [pytest.mark.all]

def pytest_configure(config):
    config.addinivalue_line(
          config.addinivalue_line("markers", "unit: mark as test unit")
    )
    config.addinivalue_line(
        "markers", "system: mark test as system"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration"
    )

@pytest.mark.unit
def test_unit():
    assert True

@pytest.mark.system
def test_system():
    assert True

@pytest.mark.integration
def test_integration():
    assert True


