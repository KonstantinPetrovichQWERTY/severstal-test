# severstal-test

I intentionally committed the .env file and settings.toml because the project is educational and needs to be quickly set up on the local machine of the reviewer. This solution is not for production purposes.

## Run
```shell
docker compose up -d
```

Known issues:

- `update_coil` may accept `delete_at` less than existed `created_at`.
