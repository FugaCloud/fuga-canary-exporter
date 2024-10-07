from ping_exporter.dns_ping import dns_ping


def test_dns_ping_without_endpoints_returns_empty_all_object(mocker):
    mocker_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mocker_argv.return_value = ({}, None)

    expected = [{'dns_server': 'all', 'status_code': 'NaN', 'ok': 0}]

    assert expected == dns_ping({})

    expected = []
    assert expected == dns_ping({}, all=False)

def test_dns_ping_with_endpoints_returns_empty_all_object(mocker):
    mocker_argv = mocker.patch('ping_exporter.main.get_config_from_argv')
    mocker_argv.return_value = ({}, None)

    rv = dns_ping({'8.8.8.8': 'google.com', '1.1.1.1': 'cloudflare.com'})

    assert rv[0]['ok'] is 1
    assert 0 == rv[0]['status_code']
