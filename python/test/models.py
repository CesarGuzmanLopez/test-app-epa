"""
Data models for T.E.S.T. results
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class EndpointResult:
    """Result from a single endpoint prediction."""

    name: str
    unit: str
    description: str
    application: str
    value: Optional[float] = None
    error: Optional[str] = None
    raw_data: Optional[Dict] = None


@dataclass
class MoleculeResult:
    """Results for a single molecule."""

    smiles: str
    properties: Dict[str, EndpointResult]


@dataclass
class TestResults:
    """Complete results from a T.E.S.T. run."""

    molecules: List[MoleculeResult]
    metadata: Dict
    diagnostics: Dict
