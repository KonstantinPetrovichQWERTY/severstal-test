import tomli


def get_service_name():
    """Retrieves the service name from project metadata."""
    try:
        name = tomli.load(open("pyproject.toml", "rb"))["project"]["name"]
    except Exception as e:
        print(e)
        name = "test-name"
    return name
