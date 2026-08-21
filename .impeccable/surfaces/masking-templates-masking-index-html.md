---
version: 1
slug: "masking-templates-masking-index-html"
primary_target: "masking/templates/masking/index.html"
related_targets: ["masking/templates/masking/base.html","masking/templates/masking/partials/_input.html","masking/templates/masking/partials/_result.html","masking/templates/masking/partials/_error.html","masking/static/masking/css/app.css","masking/static/masking/js/app.js"]
---

# Surface Brief

## Scope and Mode

- Target: `masking/templates/masking/index.html` and its frontend partials/static assets.
- Mode: Operate.

## Audience, Job, and Action

- Thai students demonstrate the masking workflow to instructors and classmates.
- User pastes log text, chooses any of five rules, runs masking, compares source/output, and copies the protected result.
- Primary action: `ปิดบังข้อมูล`.

## Content and Constraints

- Preserve existing Django/HTMX/Alpine behavior and frontend-only ownership.
- Show five assignment-defined categories without inventing backend capability.
- Keep GitHub source link and in-memory/no-storage statement visible.
- Responsive, keyboard accessible, reduced-motion safe.

## Chosen Direction

- Clean compliance dashboard: official light surface, navy typography, teal primary action, thin blue-gray rules, restrained category colors.
- Approved composition: `.impeccable/mocks/clean-compliance-a.png`.
- Memorable moment: a visible center bridge connects source text to protected output while five rule checks remain continuously scannable.
- Do not literalize generated admin identity, fabricated JSON fields, added-rule control, or fake success metrics.

## Component Grammar

- White work surfaces over a cool gray canvas; 1px blue-gray borders; 10-14px restrained corner radii.
- Low elevation: border definition first, soft shadow only on the primary workspace.
- Thai-first sans typography with compact uppercase/English product label; monospace only inside text editors.
- Controls use solid navy/teal states, clear 2px focus rings, and category color as small icon/indicator fields rather than large fills.
- Desktop: narrow rule rail plus two equal editors. Mobile: rules become a compact horizontal/stacked selector above vertically ordered editors.

## Implementation Inventory

| Ingredient | Commitment | Medium |
|---|---|---|
| Header | Product name, Thai promise, privacy state, GitHub link | Semantic HTML/CSS |
| Rule rail | Five labeled enabled controls with distinct small color marks | Form inputs + inline SVG/CSS |
| Source editor | Dominant editable surface with character count | Existing textarea + CSS |
| Transformation bridge | Clear source-to-output relationship and loading state | Semantic button/indicator + CSS |
| Protected output | Equal visual weight, live region, copy control | Existing HTMX partial + HTML/CSS/Alpine |
| Empty/result states | Useful next action, detection summary, category legend | Existing partials + HTML/CSS |
| Motion | One restrained processing sweep; none under reduced motion | CSS |

## Unresolved Decisions

- GitHub URL remains supplied by existing settings.
- Backend regex stubs may yield no detections until teammates complete their rules; frontend must explain that state without implying failure.
