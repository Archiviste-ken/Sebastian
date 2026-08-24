from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelResponse:
    content: str
    raw: Any = None


class ModelGateway:
    def generate(
        self,
        messages: list[dict[str, str]],
        response_format: dict[str, Any] | None = None,
    ) -> ModelResponse:
        raise NotImplementedError