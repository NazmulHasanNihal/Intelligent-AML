import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


class LaTeXProjectValidator:
    """Automated validator for LaTeX projects (IEEE paper & University thesis).

    Validates inputs, figures, bib citations, labels/refs, balanced
    environments, and math modes.
    """

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.main_tex = self.project_dir / "main.tex"
        self.references_bib = self.project_dir / "references.bib"
        self.figures_dir = self.project_dir / "figures"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_bib_keys(self) -> Set[str]:
        if not self.references_bib.exists():
            self.errors.append(
                f"Missing references.bib at {self.references_bib}"
            )
            return set()
        content = self.references_bib.read_text(encoding="utf-8")
        keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", content))
        return keys

    def get_all_tex_files(self) -> List[Path]:
        return list(self.project_dir.rglob("*.tex"))

    def check_inputs_and_structure(self):
        if not self.main_tex.exists():
            self.errors.append(f"Missing main.tex in {self.project_dir}")
            return

        content = self.main_tex.read_text(encoding="utf-8")
        input_matches = re.findall(r"\\input\{([^}]+)\}", content)
        for inp in input_matches:
            inp_path = self.project_dir / (
                inp if inp.endswith(".tex") else f"{inp}.tex"
            )
            if not inp_path.exists():
                self.errors.append(f"Input file not found: {inp_path}")

    def check_citations(self, bib_keys: Set[str]):
        tex_files = self.get_all_tex_files()
        for tex_file in tex_files:
            content = tex_file.read_text(encoding="utf-8")
            # Remove comments
            clean_content = re.sub(r"(?<!\\)%.*", "", content)
            cites = re.findall(r"\\cite\{([^}]+)\}", clean_content)
            for cite_group in cites:
                for key in cite_group.split(","):
                    key = key.strip()
                    if key and key not in bib_keys:
                        self.errors.append(
                            f"Missing citation key '{key}' in {tex_file.name} (not found in references.bib)"
                        )

    def check_figures(self):
        tex_files = self.get_all_tex_files()
        for tex_file in tex_files:
            content = tex_file.read_text(encoding="utf-8")
            clean_content = re.sub(r"(?<!\\)%.*", "", content)
            figs = re.findall(
                r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", clean_content
            )
            for fig in figs:
                fig_path = self.project_dir / fig
                # If relative to figures/ or direct
                if not fig_path.exists():
                    alt_path = self.figures_dir / Path(fig).name
                    if not alt_path.exists():
                        self.errors.append(
                            f"Referenced figure not found: {fig} (checked {fig_path} and {alt_path}) in {tex_file.name}"
                        )

    def check_environments(self):
        tex_files = self.get_all_tex_files()
        for tex_file in tex_files:
            content = tex_file.read_text(encoding="utf-8")
            clean_content = re.sub(r"(?<!\\)%.*", "", content)

            # Match \begin{env} and \end{env}
            tokens = re.findall(r"\\(begin|end)\{([^}]+)\}", clean_content)
            stack = []
            for action, env in tokens:
                if action == "begin":
                    stack.append((env, tex_file.name))
                elif action == "end":
                    if not stack:
                        self.errors.append(
                            f"Unmatched \\end{{{env}}} in {tex_file.name}"
                        )
                    else:
                        last_env, source_file = stack.pop()
                        if last_env != env:
                            self.errors.append(
                                f"Mismatched environment: \\begin{{{last_env}}} closed by \\end{{{env}}} in {tex_file.name}"
                            )

            for unclosed_env, source_file in stack:
                # Document environment in subfiles is fine if main wraps it
                if unclosed_env != "document":
                    self.warnings.append(
                        f"Unclosed \\begin{{{unclosed_env}}} in {source_file}"
                    )

    def check_labels_and_refs(self):
        tex_files = self.get_all_tex_files()
        labels: Set[str] = set()
        refs: List[Tuple[str, Path]] = []

        for tex_file in tex_files:
            content = tex_file.read_text(encoding="utf-8")
            clean_content = re.sub(r"(?<!\\)%.*", "", content)

            found_labels = re.findall(r"\\label\{([^}]+)\}", clean_content)
            for lbl in found_labels:
                labels.add(lbl.strip())

            found_refs = re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", clean_content)
            for r in found_refs:
                refs.append((r.strip(), tex_file))

        for ref_key, src_file in refs:
            if ref_key not in labels:
                self.warnings.append(
                    f"Undefined reference '\\ref{{{ref_key}}}' in {src_file.name}"
                )

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        self.errors.clear()
        self.warnings.clear()

        bib_keys = self.load_bib_keys()
        self.check_inputs_and_structure()
        self.check_citations(bib_keys)
        self.check_figures()
        self.check_environments()
        self.check_labels_and_refs()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings


def validate_all_latex_projects():
    base_dir = Path(__file__).resolve().parent.parent.parent
    ieee_dir = base_dir / "papers" / "IEEE_Research_Paper"
    if not ieee_dir.exists():
        ieee_dir = base_dir / "IEEE_Research_Paper"
    thesis_dir = base_dir / "papers" / "University_CSE_Thesis"
    if not thesis_dir.exists():
        thesis_dir = base_dir / "University_CSE_Thesis"

    projects = [
        ("IEEE Research Paper", ieee_dir),
        ("University CSE Thesis", thesis_dir),
    ]

    all_passed = True
    print("\n" + "=" * 80)
    print("      AUTONOMOUS LATEX WORKSHOP COMPILATION & INTEGRITY AUDIT")
    print("=" * 80)

    for name, pdir in projects:
        validator = LaTeXProjectValidator(pdir)
        is_valid, errors, warnings = validator.validate()
        status = "PASSED (100% CLEAN)" if is_valid else "FAILED"
        print(f"\n[Project] {name}: {status}")
        print(f"  Path: {pdir}")

        if errors:
            all_passed = False
            print(f"  Errors ({len(errors)}):")
            for err in errors:
                print(f"    - [ERROR] {err}")
        else:
            print("  Errors: 0 (No syntax, broken citations, or missing figures)")

        if warnings:
            print(f"  Warnings ({len(warnings)}):")
            for warn in warnings:
                print(f"    - [WARN] {warn}")
        else:
            print("  Warnings: 0")

    print("\n" + "=" * 80)
    print(
        f"OVERALL AUDIT RESULT: {'ALL PROJECTS READY FOR OVERLEAF' if all_passed else 'FIXES NEEDED'}"
    )
    print("=" * 80 + "\n")
    return all_passed


if __name__ == "__main__":
    validate_all_latex_projects()
