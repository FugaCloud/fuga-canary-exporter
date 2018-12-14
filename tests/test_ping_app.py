from ping_exporter.ping_app import index, names


def test_index_returns_page_with_link_to_metrics():
    assert -1 != index().find("metrics")


def test_prometheus_indexer_endpoint_returns_correct_info(mocker):
    mock_flask_json = mocker.patch('ping_exporter.ping_app.flask.jsonify')

    names()

    mock_flask_json.assert_called_with({'status': 'success',
                                        'data': ['probe_url',
                                                 'probe_response_time',
                                                 'probe_status_code',
                                                 'probe_ok',
                                                 'probe_exception']})


