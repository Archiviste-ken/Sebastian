from pathlib import Path

from app.config import Settings
from app.llm.groq import GroqModelGateway
from app.orchestrator import Sebastian


def main():
    workspace = Path.cwd()

    settings = Settings()

    gateway = GroqModelGateway(
        api_key=settings.groq_api_key,
        model="openai/gpt-oss-20b",
    )

    agent = Sebastian(
        workspace=workspace,
        gateway=gateway,
    )

    report = agent.run(
        "Read README.md and tell me what this project does.",
    )

    print("\n=== SEBASTIAN V1 REPORT ===\n")
    print(report)


if __name__ == "__main__":
    main()