from ping_exporter.prometheus_metrics import generate_name, lookup_attribute_to_name, lookup_type, prometheus_text


def test_generate_name_work_correctly():
    assert "test" == generate_name("test")
    assert "test{number=\"123\"}" == generate_name("test", {"number": "123"})
    assert "test{letter=\"T\",number=\"123\"}" == generate_name("test", {"number": 123, "letter": "T"})


def test_lookup_attribute_to_name():
    assert "probe_time" == lookup_attribute_to_name("time")
    assert "probe_ok" == lookup_attribute_to_name("ok")
    assert "probe_response_time" == lookup_attribute_to_name("elapsed")


def test_lookup_type():
    assert "# TYPE time gauge" == lookup_type("time")


def test_prometheus_text(mocker):
    mock_main_get_instance = mocker.patch('ping_exporter.main.get_instance_name')
    mock_main_get_instance.return_value = "testing"
    mock_main_get_config_from_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mock_main_get_config_from_argv.return_value = ({}, None)

    text_lines = prometheus_text({'endpoints': []}).splitlines()
    assert text_lines[0].startswith('# TYPE')
    assert text_lines[1].startswith('# HELP')
    assert text_lines[2].startswith('probe_')
