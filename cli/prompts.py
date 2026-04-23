import questionary

from domain.entities import PricingRequest
from domain.enums import PropertyType


def ask_pricing_request() -> PricingRequest | None:
    property_type_answer = questionary.select(
        "Qual tipo de locacao voce deseja orcar?",
        choices=[
            questionary.Choice("Apartamento", value=PropertyType.APARTMENT),
            questionary.Choice("Casa", value=PropertyType.HOUSE),
            questionary.Choice("Estudio", value=PropertyType.STUDIO),
        ],
    ).ask()

    if property_type_answer is None:
        return None

    property_type = property_type_answer
    bedrooms = 1
    has_children = False
    has_garage = False
    studio_spots = 0

    if property_type in {PropertyType.APARTMENT, PropertyType.HOUSE}:
        bedrooms = questionary.select(
            "Quantos quartos voce deseja?",
            choices=[
                questionary.Choice("1 quarto", value=1),
                questionary.Choice("2 quartos", value=2),
            ],
        ).ask()
        if bedrooms is None:
            return None

        garage_answer = questionary.confirm("Deseja incluir garagem?", default=False).ask()
        if garage_answer is None:
            return None
        has_garage = bool(garage_answer)

        if property_type is PropertyType.APARTMENT:
            children_answer = questionary.confirm(
                "Ha criancas morando no apartamento?",
                default=False,
            ).ask()
            if children_answer is None:
                return None
            has_children = bool(children_answer)
    else:
        studio_spots = questionary.text(
            "Quantas vagas o estudio precisa?",
            default="0",
            validate=lambda text: text.isdigit() or "Informe um numero inteiro maior ou igual a zero.",
        ).ask()
        if studio_spots is None:
            return None
        studio_spots = int(studio_spots)

    contract_installments = questionary.select(
        "Em quantas parcelas deseja dividir a taxa de contrato?",
        choices=[
            questionary.Choice(f"{number}x", value=number) for number in range(1, 6)
        ],
    ).ask()
    if contract_installments is None:
        return None

    return PricingRequest(
        property_type=property_type,
        bedrooms=bedrooms,
        has_children=has_children,
        has_garage=has_garage,
        studio_spots=studio_spots,
        contract_installments=contract_installments,
    )


def ask_export_csv() -> bool:
    answer = questionary.confirm(
        "Deseja gerar um arquivo CSV com este orcamento?",
        default=True,
    ).ask()
    return False if answer is None else bool(answer)


def ask_export_path() -> str | None:
    return questionary.text(
        "Informe o nome do arquivo CSV",
        default="orcamento.csv",
        validate=lambda text: bool(text.strip()) or "Digite um nome de arquivo valido.",
    ).ask()
