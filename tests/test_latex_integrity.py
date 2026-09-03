from pathlib import Path
from src.utils.latex_validator import LaTeXProjectValidator

BASE_DIR = Path(__file__).resolve().parent.parent


def test_ieee_research_paper_integrity():
    project_dir = BASE_DIR / "papers" / "IEEE_Research_Paper"
    if not project_dir.exists():
        project_dir = BASE_DIR / "IEEE_Research_Paper"
    validator = LaTeXProjectValidator(project_dir)
    is_valid, errors, warnings = validator.validate()
    assert is_valid, f"IEEE Research Paper has LaTeX errors: {errors}"
    assert len(warnings) == 0, f"IEEE Research Paper has LaTeX warnings: {warnings}"


def test_university_cse_thesis_integrity():
    project_dir = BASE_DIR / "papers" / "University_CSE_Thesis"
    if not project_dir.exists():
        project_dir = BASE_DIR / "University_CSE_Thesis"
    validator = LaTeXProjectValidator(project_dir)
    is_valid, errors, warnings = validator.validate()
    assert is_valid, f"University CSE Thesis has LaTeX errors: {errors}"
    assert len(warnings) == 0, f"University CSE Thesis has LaTeX warnings: {warnings}"
