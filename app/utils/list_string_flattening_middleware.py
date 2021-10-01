from starlette.types import ASGIApp, Scope, Receive, Send
from urllib.parse import parse_qs as parse_query_string
from urllib.parse import urlencode as encode_query_string

# Imported from https://github.com/tiangolo/fastapi/issues/50#issuecomment-910974661
# Thanks to allenhumphreys


class QueryStringFlatteningMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        query_string = scope.get("query_string", None).decode()
        if scope["type"] == "http" and query_string:
            parsed = parse_query_string(query_string)
            flattened = {}
            for name, values in parsed.items():
                all_values = []
                for value in values:
                    all_values.extend(value.split(","))

                flattened[name] = all_values

            # doseq: Turn lists into repeated parameters, which is better for FastAPI
            scope["query_string"] = encode_query_string(flattened, doseq=True).encode("utf-8")

            await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
