from aiohttp import web
import urllib.parse
from conf import settings

ROUTER = {
    "link-request": {
        "url": "/account",
        "GET": "request_handle.redeem_product",
    },
}


def generate_routes() -> list:
    routes = []
    for key, value in ROUTER.items():

        if "GET" in value:
            handler = value["GET"]
            routes.append(
                web.get(value["url"], object_at_end_of_path(handler), name=f"get-{key}")
            )

        if "PUT" in value:
            handler = value["PUT"]
            routes.append(
                web.put(value["url"], object_at_end_of_path(handler), name=f"put-{key}")
            )

        if "POST" in value:
            handler = value["POST"]
            routes.append(
                web.post(
                    value["url"], object_at_end_of_path(handler), name=f"post-{key}"
                )
            )

        if "DELETE" in value:
            handler = value["DELETE"]
            routes.append(
                web.delete(
                    value["url"], object_at_end_of_path(handler), name=f"delete-{key}"
                )
            )
    return routes


def reverse(name: str, **kwargs) -> str:
    return urllib.parse.urljoin(
        settings.APP.BASE_URL,
        urllib.parse.quote_plus("." + ROUTER[name]["url"].format(**kwargs), safe="/"),
    )


def object_at_end_of_path(path):
    """Attempt to return the Python object at the end of the dotted
    path by repeated imports and attribute access.
    """
    access_path = path.split(".")
    module = None
    for index in range(1, len(access_path)):
        try:
            # import top level module
            module_name = ".".join(access_path[:-index])
            module = __import__(module_name)
        except ImportError:
            continue
        else:
            for step in access_path[1:-1]:  # walk down it
                module = getattr(module, step)
            break
    if module:
        return getattr(module, access_path[-1])
    else:
        return globals()["__builtins__"][path]
