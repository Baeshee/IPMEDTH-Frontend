"""Exceptions for IPMEDTH application."""


class ApplicationError(Exception):
    """Generic Application exception."""


class NoMeasurementsError(ApplicationError):
    """No Measurements exception."""
