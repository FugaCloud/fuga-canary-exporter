import pytest

from ping_exporter.main import check_config, ConfigException


def test_required_config_check_works():
    valid_config = {"endpoints": []}
    check_config(valid_config)

    invalid_config = {}

    with pytest.raises(ConfigException):
        check_config(invalid_config)
