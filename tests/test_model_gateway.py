import pytest

from app.llm.gateway import ModelGateway


def test_base_model_gateway_is_not_implemented():
    gateway = ModelGateway()

    with pytest.raises(NotImplementedError):
        gateway.generate(
            [
                {
                    "role": "user",
                    "content": "Hello Sebastian",
                }
            ]
        )