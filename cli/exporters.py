import csv
from pathlib import Path

from domain.entities import BudgetResult


def export_budget_to_csv(result: BudgetResult, file_name: str) -> str:
    path = Path(file_name).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["parcela", "aluguel_mensal", "parcela_contrato", "total_mes"])
        for installment in result.monthly_installments:
            writer.writerow(
                [
                    installment.month,
                    f"{installment.monthly_rent:.2f}",
                    f"{installment.contract_installment:.2f}",
                    f"{installment.total_due:.2f}",
                ]
            )

    return str(path)
