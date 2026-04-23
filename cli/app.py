from .controllers import run_budget_flow
from .presenters import show_banner


def run() -> None:
    show_banner()
    run_budget_flow()
