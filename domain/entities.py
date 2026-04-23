from dataclasses import dataclass, field

from .enums import PropertyType
from .exceptions import InvalidPricingRequest


@dataclass(frozen=True, slots=True)
class Contract:
    total_fee: float
    installments: int
    max_installments: int = 5

    def validate(self) -> None:
        if not 1 <= self.installments <= self.max_installments:
            raise InvalidPricingRequest(
                f"O contrato aceita de 1 a {self.max_installments} parcelas."
            )

    @property
    def installment_amount(self) -> float:
        return self.total_fee / self.installments


@dataclass(slots=True)
class PricingRequest:
    property_type: PropertyType
    contract_installments: int
    bedrooms: int = 1
    has_children: bool = False
    has_garage: bool = False
    studio_spots: int = 0

    def validate(self) -> None:
        self.contract.validate()

        if self.property_type.accepts_bedrooms and self.bedrooms not in {1, 2}:
            raise InvalidPricingRequest("Apartamento e casa aceitam apenas 1 ou 2 quartos.")

        if not self.property_type.accepts_bedrooms and self.bedrooms != 1:
            raise InvalidPricingRequest("Estudio nao utiliza configuracao de quartos.")

        if self.property_type.uses_spot_count:
            if self.has_garage:
                raise InvalidPricingRequest("Estudio utiliza contagem de vagas, nao a flag de garagem.")
            if self.studio_spots < 0:
                raise InvalidPricingRequest("O numero de vagas nao pode ser negativo.")
            return

        if self.studio_spots:
            raise InvalidPricingRequest("Numero de vagas do estudio nao se aplica a esse imovel.")

    @property
    def contract(self) -> Contract:
        return Contract(total_fee=2000.0, installments=self.contract_installments)

    def create_property(self) -> "RentalProperty":
        if self.property_type is PropertyType.APARTMENT:
            return Apartment(bedrooms=self.bedrooms, has_children=self.has_children, has_garage=self.has_garage)
        if self.property_type is PropertyType.HOUSE:
            return House(bedrooms=self.bedrooms, has_garage=self.has_garage)
        return Studio(spots=self.studio_spots)


@dataclass(slots=True)
class BudgetLineItem:
    description: str
    amount: float
    kind: str = "charge"


@dataclass(slots=True)
class MonthlyInstallment:
    month: int
    monthly_rent: float
    contract_installment: float
    total_due: float


@dataclass(slots=True)
class BudgetResult:
    property_type: PropertyType
    monthly_subtotal: float
    discount_amount: float
    monthly_total: float
    contract_fee_total: float
    contract_installments: int
    contract_installment_amount: float
    line_items: list[BudgetLineItem] = field(default_factory=list)

    @classmethod
    def from_request(cls, request: PricingRequest) -> "BudgetResult":
        request.validate()

        rental_property = request.create_property()
        monthly_subtotal = rental_property.monthly_subtotal
        discount_amount = rental_property.discount_amount

        return cls(
            property_type=request.property_type,
            monthly_subtotal=monthly_subtotal,
            discount_amount=discount_amount,
            monthly_total=monthly_subtotal - discount_amount,
            contract_fee_total=request.contract.total_fee,
            contract_installments=request.contract.installments,
            contract_installment_amount=request.contract.installment_amount,
            line_items=rental_property.line_items,
        )

    @property
    def monthly_installments(self) -> list[MonthlyInstallment]:
        installments: list[MonthlyInstallment] = []
        for month in range(1, 13):
            contract_installment = (
                self.contract_installment_amount if month <= self.contract_installments else 0.0
            )
            installments.append(
                MonthlyInstallment(
                    month=month,
                    monthly_rent=self.monthly_total,
                    contract_installment=contract_installment,
                    total_due=self.monthly_total + contract_installment,
                )
            )
        return installments


@dataclass(slots=True)
class RentalProperty:
    property_type: PropertyType

    @property
    def line_items(self) -> list[BudgetLineItem]:
        raise NotImplementedError

    @property
    def monthly_subtotal(self) -> float:
        return sum(item.amount for item in self.line_items if item.kind == "charge")

    @property
    def discount_amount(self) -> float:
        return 0.0


@dataclass(slots=True)
class Apartment(RentalProperty):
    bedrooms: int
    has_children: bool
    has_garage: bool

    BASE_PRICE = 700.0
    TWO_BEDROOMS_EXTRA = 200.0
    GARAGE_PRICE = 300.0
    DISCOUNT_RATE = 0.05

    def __init__(self, bedrooms: int, has_children: bool, has_garage: bool) -> None:
        super().__init__(property_type=PropertyType.APARTMENT)
        self.bedrooms = bedrooms
        self.has_children = has_children
        self.has_garage = has_garage

    @property
    def line_items(self) -> list[BudgetLineItem]:
        items = [BudgetLineItem("Aluguel base do apartamento (1 quarto)", self.BASE_PRICE)]
        if self.bedrooms == 2:
            items.append(
                BudgetLineItem("Adicional por segundo quarto do apartamento", self.TWO_BEDROOMS_EXTRA)
            )
        if self.has_garage:
            items.append(BudgetLineItem("Garagem", self.GARAGE_PRICE))
        return items

    @property
    def discount_amount(self) -> float:
        if self.has_children:
            return 0.0
        return self.monthly_subtotal * self.DISCOUNT_RATE


@dataclass(slots=True)
class House(RentalProperty):
    bedrooms: int
    has_garage: bool

    BASE_PRICE = 900.0
    TWO_BEDROOMS_EXTRA = 250.0
    GARAGE_PRICE = 300.0

    def __init__(self, bedrooms: int, has_garage: bool) -> None:
        super().__init__(property_type=PropertyType.HOUSE)
        self.bedrooms = bedrooms
        self.has_garage = has_garage

    @property
    def line_items(self) -> list[BudgetLineItem]:
        items = [BudgetLineItem("Aluguel base da casa (1 quarto)", self.BASE_PRICE)]
        if self.bedrooms == 2:
            items.append(BudgetLineItem("Adicional por segundo quarto da casa", self.TWO_BEDROOMS_EXTRA))
        if self.has_garage:
            items.append(BudgetLineItem("Garagem", self.GARAGE_PRICE))
        return items


@dataclass(slots=True)
class Studio(RentalProperty):
    spots: int

    BASE_PRICE = 1200.0
    TWO_SPOTS_PRICE = 250.0
    EXTRA_SPOT_PRICE = 60.0

    def __init__(self, spots: int) -> None:
        super().__init__(property_type=PropertyType.STUDIO)
        self.spots = spots

    @property
    def line_items(self) -> list[BudgetLineItem]:
        items = [BudgetLineItem("Aluguel base do estudio", self.BASE_PRICE)]
        parking_price = self._parking_price()
        if parking_price:
            items.append(
                BudgetLineItem(
                    f"Vagas de garagem do estudio ({self.spots} vaga(s))",
                    parking_price,
                )
            )
        return items

    def _parking_price(self) -> float:
        if self.spots <= 0:
            return 0.0
        if self.spots <= 2:
            return self.TWO_SPOTS_PRICE
        extra_spots = self.spots - 2
        return self.TWO_SPOTS_PRICE + (extra_spots * self.EXTRA_SPOT_PRICE)
