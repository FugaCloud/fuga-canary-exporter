# Ping exporter

A prometheus exporter that makes get requests to the different endpoints given in the configuration. The exporter has a 'instance_name' field in the configuration so that this exporter can be run on multiple servers and later can be differentiated. If that last point is not a requirement just use the standard prometheus blackbox exporter.

For a quick test run:

```sh
docker-compose up --build
```

### Handy commands:

```sh
gunicorn 'ping_exporter.main:make_app(**{"config":"configuration.yaml"})'
```

For debug purposes run exporter with the flask debug server:

```sh
PYTHONPATH=. python ping_exporter/main.py
```

Generate an example config with:

```sh
PYTHONPATH=. python ping_exporter/main.py --generate_config > example-config.yaml
```

Small side note: if the configuration is updated when the program is running, it will automatically use the new configuration without restarting.
