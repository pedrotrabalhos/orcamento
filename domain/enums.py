from enum import Enum


class PropertyType(str, Enum):
    APARTMENT = "apartamento"
    HOUSE = "casa"
    STUDIO = "estudio"

    @property
    def label(self) -> str:
        labels = {
            PropertyType.APARTMENT: "Apartamento",
            PropertyType.HOUSE: "Casa",
            PropertyType.STUDIO: "Estudio",
        }
        return labels[self]

    @property
    def accepts_bedrooms(self) -> bool:
        return self in {PropertyType.APARTMENT, PropertyType.HOUSE}

    @property
    def uses_spot_count(self) -> bool:
        return self is PropertyType.STUDIO
