from ping_exporter.ping import pong


def test_pong_without_endpoints_returns_empty_all_object(mocker):
    mocker_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mocker_argv.return_value = ({}, None)

    expected = [{'url': 'all', 'elapsed': 0,
                 'status_code': 'Nan', 'ok': 0, 'exception': 0}]

    assert expected == pong([])

    expected = []
    assert expected == pong([], all=False)


def test_pong_against_mock_server_returns_wanted_data(mocker, httpserver):
    mocker_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mocker_argv.return_value = ({}, None)

    rv = pong([httpserver.url])

    assert rv[0]['elapsed'] == rv[1]['elapsed']
    assert 1 == rv[0]['ok']
    assert 0 == rv[0]['exception']
    assert 204 == rv[0]['status_code']
    assert isinstance(rv[0]['elapsed'], float)


def test_pong_against_mock_server_returns_wanted_unserialized_data(
        mocker, httpserver):
    mocker_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mocker_argv.return_value = ({}, None)

    rv = pong([httpserver.url], serialize=False)

    assert rv[0]['elapsed'] == rv[1]['elapsed']
    assert rv[0]['ok'] is True
    assert rv[0]['exception'] is None
    assert 204 == rv[0]['status_code']
    assert isinstance(rv[0]['elapsed'], float)


def test_pong_time_out_returns_exception_equals_one(mocker, httpserver):
    mocker_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mocker_argv.return_value = ({"time_out": 0.0}, None)

    rv = pong([httpserver.url])

    assert 0 == rv[0]['ok']
    assert 1 == rv[0]['exception']
    assert httpserver.url == rv[0]['url']
    assert 'Nan' == rv[0]['status_code']
