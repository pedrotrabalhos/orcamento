class DomainError(Exception):
    """Erro base da camada de dominio."""


class InvalidPricingRequest(DomainError):
    """Lancado quando os dados de entrada sao invalidos para o calculo."""
