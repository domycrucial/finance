#!/usr/bin/env python3
"""Validates all skills in .agents/skills/ against Antigravity SKILL.md standards."""
import re
import sys
from pathlib import Path

def validate_skills(skills_dir: Path) -> int:
    errors = []
    skill_folders = sorted([p for p in skills_dir.iterdir() if p.is_dir()])
    if not skill_folders:
        print(f"No skill folders found in {skills_dir}")
        return 1

    for folder in skill_folders:
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{folder.name}: Missing SKILL.md")
            continue

        content = skill_md.read_text(encoding="utf-8")
        lines = content.splitlines()
        if len(lines) > 500:
            errors.append(f"{folder.name}: SKILL.md exceeds 500 lines ({len(lines)})")

        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            errors.append(f"{folder.name}: Missing or malformed YAML frontmatter")
            continue

        fm = match.group(1)
        name_m = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
        desc_m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)

        if not name_m:
            errors.append(f"{folder.name}: Frontmatter missing 'name'")
        else:
            name_val = name_m.group(1).strip().strip("'\"")
            if name_val != folder.name:
                errors.append(f"{folder.name}: Frontmatter name '{name_val}' != folder name '{folder.name}'")
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name_val):
                errors.append(f"{folder.name}: Invalid kebab-case name '{name_val}'")

        if not desc_m:
            errors.append(f"{folder.name}: Frontmatter missing 'description'")
        else:
            desc_val = desc_m.group(1).strip().strip("'\"")
            if len(desc_val) > 1024 or len(desc_val) < 20:
                errors.append(f"{folder.name}: Description length {len(desc_val)} out of range (20..1024)")

        # Verify referenced local files exist
        for ref in re.findall(r"`(resources/[a-zA-Z0-9_.-]+)`", content):
            if not (folder / ref).exists():
                errors.append(f"{folder.name}: Referenced file '{ref}' does not exist")

        print(f"[OK] {folder.name} ({len(lines)} lines)")

    if errors:
        print("\nValidation Errors:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"\nAll {len(skill_folders)} skills passed validation!")
    return 0

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".agents/skills")
    raise SystemExit(validate_skills(target))
