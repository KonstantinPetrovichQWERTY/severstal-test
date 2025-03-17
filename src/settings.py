from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(settings_files=["settings.toml"], environments=True)
