from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from domain.entities import BudgetResult


console = Console()


def show_banner() -> None:
    console.print(
        Panel.fit(
            "[bold cyan]Sistema de Orcamento de Aluguel[/bold cyan]\n"
            "[white]Monte um orcamento e exporte o resultado em CSV.[/white]",
            border_style="cyan",
        )
    )


def show_loading_message() -> None:
    console.print("[yellow]Processando orcamento...[/yellow]")


def show_budget_result(result: BudgetResult) -> None:
    table = Table(title="Resumo do Orcamento", header_style="bold green")
    table.add_column("Item")
    table.add_column("Valor", justify="right")

    for item in result.line_items:
        table.add_row(item.description, _format_currency(item.amount))

    table.add_row("Subtotal mensal", _format_currency(result.monthly_subtotal))
    table.add_row("Desconto", _format_currency(-result.discount_amount) if result.discount_amount else "R$ 0,00")
    table.add_row("Total mensal", f"[bold]{_format_currency(result.monthly_total)}[/bold]")
    table.add_row(
        f"Taxa de contrato ({result.contract_installments}x)",
        _format_currency(result.contract_installment_amount),
    )
    table.add_row("Taxa de contrato total", _format_currency(result.contract_fee_total))

    console.print(table)


def show_successful_export(path: str) -> None:
    console.print(f"[green]CSV gerado com sucesso em:[/green] {path}")


def show_message(message: str, style: str = "white") -> None:
    console.print(f"[{style}]{message}[/{style}]")


def _format_currency(value: float) -> str:
    rounded = f"{value:,.2f}"
    normalized = rounded.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {normalized}"
