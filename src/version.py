import tomli

try:
    __version__ = tomli.load(open("pyproject.toml", "rb"))["project"]["version"]
except Exception as e:
    print(e)
    __version__ = "test"
