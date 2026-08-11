"""Shared precipitation and ionospheric-conductance calculations."""

from .robinson import hall, halluncertainty, ped, peduncertainty

__all__ = ["ped", "hall", "peduncertainty", "halluncertainty"]

