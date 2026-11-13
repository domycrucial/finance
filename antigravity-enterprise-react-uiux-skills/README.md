# Enterprise React UI/UX Skills Library for Google Antigravity

A complete, modular 8-skill library covering **Web (React + Tailwind/Radix) & Mobile (React Native)** with **Enterprise** standards across the full UI/UX lifecycle.

## Directory Structure

```text
antigravity-enterprise-react-uiux-skills/
├── .agents/
│   └── skills/
│       ├── ui-design-tokens/
│       │   ├── SKILL.md
│       │   └── resources/ (tokens-schema.json, tailwind-rn-bridge.md)
│       ├── ui-component-architecture/
│       │   ├── SKILL.md
│       │   └── resources/ (component-patterns.tsx, platform-parity-matrix.md)
│       ├── ui-layout-responsive/
│       │   ├── SKILL.md
│       │   └── resources/ (app-shell-patterns.md, density-breakpoints.md)
│       ├── ui-accessibility-wcag/
│       │   ├── SKILL.md
│       │   └── resources/ (wcag-22-checklist.md, aria-keyboard-patterns.md)
│       ├── ui-enterprise-data-tables/
│       │   ├── SKILL.md
│       │   └── resources/ (tanstack-table-recipe.tsx, dataviz-standards.md)
│       ├── ui-forms-workflows/
│       │   ├── SKILL.md
│       │   └── resources/ (rhf-zod-wizard.tsx, rbac-validation-rules.md)
│       ├── ui-motion-feedback/
│       │   ├── SKILL.md
│       │   └── resources/ (resilience-states.md, motion-tokens.md)
│       └── ux-audit-heuristics/
│           ├── SKILL.md
│           └── resources/ (heuristic-rubric.md, audit-report-template.md)
├── scripts/
│   ├── validate-skills.py
│   └── ui-test-setup.md
├── install.ps1
├── install.sh
└── README.md
```

## Installation in Google Antigravity

Antigravity discovers skills from two official locations:
- **Workspace-specific (recommended for team repos):** `<workspace-root>/.agents/skills/<skill-name>/`
- **Global (all projects):** `~/.gemini/config/skills/<skill-name>/` (Windows: `%USERPROFILE%\.gemini\config\skills\<skill-name>\`)

### Windows (PowerShell)
```powershell
# Workspace install (run from your React project root, or pass -WorkspacePath)
.\install.ps1 -Scope Workspace -WorkspacePath "C:\path\to\your-react-app"

# Global install (available in all Antigravity projects)
.\install.ps1 -Scope Global
```

### macOS / Linux (Bash)
```bash
chmod +x install.sh
# Workspace install
./install.sh workspace /path/to/your-react-app

# Global install
./install.sh global
```

### Reloading in Antigravity
- **Antigravity IDE**: Open the **Customizations** menu in the agent side panel to verify all 8 skills are active.
- **Antigravity CLI**: Run `/skills reload` or start a new conversation.

# Automated UI/UX & Skill Testing Procedures

## 1. Skill Manifest & Structure Validation
Run the bundled validator before committing or installing:
```bash
python3 scripts/validate-skills.py .agents/skills
```

## 2. Antigravity Skill Activation & Trigger Testing
Open Antigravity IDE or CLI (`agy`) in a project with `.agents/skills/` installed:
1. **Discovery Check**: Open the Antigravity Customizations panel (IDE) or type `/` (CLI) and confirm all 8 skills appear (`ui-design-tokens`, `ui-component-architecture`, `ui-layout-responsive`, `ui-accessibility-wcag`, `ui-enterprise-data-tables`, `ui-forms-workflows`, `ui-motion-feedback`, `ux-audit-heuristics`).
2. **Autonomous Trigger Test**: Run these prompts in a fresh chat and verify the agent reads the matching `SKILL.md`:
   - *"Create a dark/light semantic token theme for React web and React Native"* -> activates `ui-design-tokens`
   - *"Build an accessible TanStack Table with server-side sorting and bulk actions"* -> activates `ui-enterprise-data-tables` + `ui-accessibility-wcag`
   - *"Audit this checkout component for WCAG 2.2 and usability issues"* -> activates `ux-audit-heuristics` + `ui-accessibility-wcag`
3. **Explicit Slash Invocation**: Run `/ui-forms-workflows Build a 3-step onboarding wizard with Zod`.

## 3. React Web & Mobile UI/UX Automated Test Suite

Install test dependencies in your React project:
```bash
npm install -D vitest @testing-library/react @testing-library/user-event vitest-axe @playwright/test @axe-core/playwright
```

### Accessibility Unit Test (Vitest + vitest-axe)
```tsx
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import { Button } from './Button';

test('Button has no WCAG accessibility violations', async () => {
  const { container } = render(<Button variant="primary">Save</Button>);
  expect(await axe(container)).toHaveNoViolations();
});
```

### E2E Keyboard & Responsive Viewport Test (Playwright)
```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('Enterprise dashboard passes WCAG 2.2 AA on desktop and mobile', async ({ page }) => {
  for (const viewport of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
    await page.setViewportSize(viewport);
    await page.goto('/');
    const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    expect(hasOverflow).toBe(false);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag22aa']).analyze();
    expect(results.violations).toEqual([]);
  }
});
```
