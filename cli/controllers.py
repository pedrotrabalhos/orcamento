from time import sleep

from domain.entities import BudgetResult
from domain.exceptions import DomainError

from .exporters import export_budget_to_csv
from .presenters import (
    show_budget_result,
    show_loading_message,
    show_message,
    show_successful_export,
)
from .prompts import ask_export_csv, ask_export_path, ask_pricing_request


def run_budget_flow() -> None:
    request = ask_pricing_request()
    if request is None:
        show_message("Operacao cancelada pelo usuario.", style="yellow")
        return

    show_loading_message()
    sleep(0.8)

    try:
        result = BudgetResult.from_request(request)
    except DomainError as exc:
        show_message(str(exc), style="red")
        return

    show_budget_result(result)

    if not ask_export_csv():
        return

    file_name = ask_export_path()
    if not file_name:
        show_message("Exportacao cancelada.", style="yellow")
        return

    exported_path = export_budget_to_csv(result, file_name)
    show_successful_export(exported_path)
