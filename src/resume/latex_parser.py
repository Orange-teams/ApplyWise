import re
from dataclasses import dataclass, field
from typing import List, Dict, Any


# ----------------------------
# Data structures
# ----------------------------

@dataclass
class ExperienceBlock:
    title: str
    duration: str
    company: str
    location: str
    bullets: List[str] = field(default_factory=list)


@dataclass
class CVData:
    profile: str = ""
    skills: Dict[str, str] = field(default_factory=dict)
    experience: List[ExperienceBlock] = field(default_factory=list)
    projects: Dict[str, List[str]] = field(default_factory=dict)
    education: List[str] = field(default_factory=list)


# ----------------------------
# Helpers
# ----------------------------

ROLE_PATTERN = re.compile(
    r"\\role\{(.+?)\}\{(.+?)\}\{(.+?)\}\{(.+?)\}",
    re.DOTALL
)

ITEMIZE_BLOCK_PATTERN = re.compile(
    r"\\begin\{itemize\}(.*?)\\end\{itemize\}",
    re.DOTALL
)

CVITEM_PATTERN = re.compile(
    r"\\cvitem\{(.*?)\}",
    re.DOTALL
)

SECTION_PATTERN = re.compile(
    r"\\section\*\{(.+?)\}",
)


# ----------------------------
# Parser
# ----------------------------

class LatexCVParser:

    def parse(self, latex: str) -> CVData:
        cv = CVData()

        # 1. Profile section
        cv.profile = self._extract_section(latex, "Profile")

        # 2. Skills section (raw text for now)
        cv.skills["raw"] = self._extract_section(latex, "Knowledge \\& Skills")

        # 3. Experience
        cv.experience = self._parse_experience(latex)

        # 4. Projects
        cv.projects = self._parse_projects(latex)

        # 5. Education
        cv.education = self._extract_itemized_section(latex, "Education")

        return cv

    # ----------------------------
    # Section extraction
    # ----------------------------

    def _extract_section(self, latex: str, name: str) -> str:
        pattern = rf"\\section\*\{{{re.escape(name)}\}}(.*?)(?=\\section|\Z)"
        match = re.search(pattern, latex, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _extract_itemized_section(self, latex: str, name: str) -> List[str]:
        section = self._extract_section(latex, name)
        items = re.findall(r"\\cvitem\{(.*?)\}", section, re.DOTALL)
        return [i.strip() for i in items]

    # ----------------------------
    # Experience parsing
    # ----------------------------

    def _parse_experience(self, latex: str) -> List[ExperienceBlock]:
        experiences = []

        role_matches = ROLE_PATTERN.finditer(latex)

        for role in role_matches:
            title, duration, company, location = role.groups()

            # Find itemize block AFTER this role
            start_idx = role.end()
            itemize_match = ITEMIZE_BLOCK_PATTERN.search(latex, start_idx)

            bullets = []
            if itemize_match:
                block = itemize_match.group(1)
                bullets = CVITEM_PATTERN.findall(block)

            experiences.append(
                ExperienceBlock(
                    title=title.strip(),
                    duration=duration.strip(),
                    company=company.strip(),
                    location=location.strip(),
                    bullets=[b.strip() for b in bullets]
                )
            )

        return experiences

    # ----------------------------
    # Projects parsing (simplified)
    # ----------------------------

    def _parse_projects(self, latex: str) -> Dict[str, List[str]]:
        section = self._extract_section(latex, "Selected Projects")

        projects = {}
        parts = re.split(r"\\textbf\{(.+?)\}", section)

        # naive grouping: title → bullets
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            body = parts[i + 1] if i + 1 < len(parts) else ""

            bullets = re.findall(r"\\cvitem\{(.*?)\}", body, re.DOTALL)

            projects[title] = [b.strip() for b in bullets]

        return projects