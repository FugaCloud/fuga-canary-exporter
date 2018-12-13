
For a quick test run:

```sh
docker-compose up --build
```


Handy commands:

```sh
gunicorn 'ping_exporter.main:make_app(**{"config":"configuration.yaml", "instance-name":"guido"})'
```

```sh
PYTHONPATH=. python ping_exporter/main.py
```

```sh
PYTHONPATH=. python ping_exporter/main.py --generate_config > example-config.yaml
```

Small side note: if the configuration is updated when the program is running, it will automatically use the new configuration without restarting.
