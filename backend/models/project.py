from dataclasses import dataclass


@dataclass
class RenovationProject:
    name: str
    budget: float

    extension_size: float = 0.0
    kitchen_spec: str = "standard"
    bathroom_spec: str = "standard"

    flooring_area: float = 0.0
    electrical_work: bool = False
    plumbing_work: bool = False
    plastering_work: bool = False
    painting_work: bool = False

    windows_doors: int = 0
    structural_work: bool = False
    roofing_work: bool = False
    landscaping_area: float = 0.0