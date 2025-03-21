# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-03-17

### Fixed

- `update_coil` not accept `delete_at` be less than existed `created_at`


## [0.4.0] - 2025-03-17

### Added

- Add Mypy checks to CI.
- Add logger middleware and local method logging.
- Add `Dockerfile` and `docker-compose.yml`.
- Add `.env` file to quick set up. This solution is not for production purposes.
- Add docstrins.

### Fixed

- Fix Mypy errors in `models.py`, `abstract_data_storage.py`, `dao.py`, `database.py`.

### Changed

- New dependencies: "pytest (^8.3.5)", pytest-asyncio = (^0.25.3)".

## [0.3.0] - 2025-03-16

### Added

- Add abstract class `DataStorage`.
- Add `DataStorage` implementation to Postgres databases `CoilPostgreDAO`.
- Add new exceptions `CoilNotFoundException` raises in DAO.

### Fixed

- Add constraints to data in schemas and model.
Numerical values must be greater than zero. Date `deleted_at` must be greater than `created_at`.
- Make `created_at` not nullable.
- Change endpoints use DAO.

### Removed

- Remove static decorators from DAO, bacause they limit abstract logic (not raises exception if some methods not implemented). 

## [0.2.0] - 2025-03-16

### Added

- Add schemas.
- Add github Actions CI for linter checks.
- Add new endpoints: `get_coil_by_id`, `update_coil`, `get_all_coils`, `delete_coil`, `get_coil_stats`.
- Add flake8 configuration.

### Fixed

- Make `deleted_at` and `created_at` nullable.
- Add timezones to dates.
- Make numerical values of type float, not integer.

### Changed

- New dependencies: "tomli (>=2.2.1,<3.0.0)", "pytz (>=2025.1,<2026.0)", "flake8 (^7.1.2)", "mypy (^1.15.0)".

### Removed

- Test endpoint `read_root`.

## [0.1.0] - 2025-03-15

### Added

- Init project.
- Project structure.
- Healthcheck endpoint. 
- Database configuration.
- Alembic migration.
- First endpoint POST `/api/v1/bags/register_new_coil/`.
