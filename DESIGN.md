---
name: PDPA Masking
description: A calm Thai-first compliance workbench for inspecting privacy transformations.
colors:
  canvas: "#f4f7fa"
  surface: "#ffffff"
  surface-soft: "#f8fafc"
  ink: "#122b50"
  ink-strong: "#0a2349"
  muted: "#5d6f89"
  quiet: "#8794a8"
  line: "#d8e0ea"
  line-strong: "#c4cfdd"
  primary: "#087f9d"
  primary-hover: "#066b86"
  primary-soft: "#e6f6f8"
  success: "#14956f"
  success-soft: "#e8f8f2"
  danger: "#c53d4d"
  danger-soft: "#fff0f2"
  focus: "#1477d4"
  credit-card: "#1784d9"
  credit-card-soft: "#e8f3ff"
  phone: "#dc8a12"
  phone-soft: "#fff3d9"
  email: "#d94a64"
  email-soft: "#ffe9ee"
  dob: "#7862cc"
  dob-soft: "#eeeafd"
  address: "#138f6d"
  address-soft: "#e4f7f0"
typography:
  headline:
    fontFamily: "Noto Sans Thai, Leelawadee UI, Tahoma, sans-serif"
    fontSize: "clamp(1.32rem, 2vw, 1.7rem)"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Noto Sans Thai, Leelawadee UI, Tahoma, sans-serif"
    fontSize: "1rem"
    fontWeight: 700
    lineHeight: 1.55
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Noto Sans Thai, Leelawadee UI, Tahoma, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Noto Sans Thai, Leelawadee UI, Tahoma, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 600
    lineHeight: 1.4
  code:
    fontFamily: "IBM Plex Mono, Consolas, monospace"
    fontSize: "0.82rem"
    fontWeight: 400
    lineHeight: "1.85rem"
rounded:
  highlight: "4px"
  badge: "6px"
  control: "8px"
  action: "10px"
  panel: "12px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  2xl: "28px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.action}"
    padding: "9px 16px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.surface}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.action}"
    padding: "9px 16px"
    height: "44px"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
  input-code:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    padding: "16px 18px"
---

# Design System: PDPA Masking

## Overview

**Creative North Star: "The Compliance Workbench"**

The system presents privacy masking as a clear before-and-after inspection. It should feel clean, official, easy, and presentation-ready: cool white working surfaces sit on a pale canvas, navy type establishes calm authority, and restrained teal identifies the primary action.

Information structure creates the visual interest. Fine rules, aligned editor geometry, a continuously visible rules rail, and a compact transformation bridge make the process legible without turning the product into a theatrical cyber dashboard. Components are refined and restrained; subtle depth may be ambient or structural, never decorative.

**Key Characteristics:**
- Cool white layered work surfaces with navy clarity.
- Teal reserved for action, privacy state, and workflow continuity.
- Fine blue-gray rules organize dense operational content.
- Five category colors appear as small semantic indicators, not large fills.
- Equal source and protected editors make transformation visible at a glance.

## Colors

The palette is a cool compliance neutral system sharpened by navy, controlled teal, and five restrained identification colors.

### Primary
- **Workbench Teal:** Carries the primary masking action, workflow indicators, active informational accents, and the product mark.
- **Deep Action Teal:** Provides hover emphasis without changing the system's calm character.
- **Teal Wash:** Supports icons and quiet informational fields without competing with task content.

### Secondary
- **Verified Green:** Communicates successful masking, safe output, and the truthful no-storage state.
- **Alert Crimson:** Appears only for errors and destructive-status language.

### Tertiary
- **Category Blue, Amber, Rose, Violet, and Green:** Distinguish credit card, phone, email, date of birth, and address through small marks, icons, toggles, chips, and inline highlights.

### Neutral
- **Cool Canvas:** Frames the workspace and separates it from white work surfaces.
- **Work Surface:** Holds panels, controls, header, legend, and footer-adjacent structures.
- **Soft Surface:** Provides low-contrast hover and supporting regions.
- **Compliance Navy:** Serves primary body text and operational labels.
- **Authority Navy:** Anchors headings and high-priority copy.
- **Muted Slate and Quiet Slate:** Carry explanatory and tertiary copy.
- **Fine Rule and Strong Rule:** Define structure before shadow is introduced.

### Named Rules

**The Restrained Signal Rule.** Category colors identify data types only in compact fields; they never become panel backgrounds or competing calls to action.

**The One Action Voice Rule.** Teal owns the primary workflow action; navy and white controls remain secondary.

## Typography

**Display Font:** Noto Sans Thai (with Leelawadee UI, Tahoma, sans-serif fallbacks)  
**Body Font:** Noto Sans Thai (with Leelawadee UI, Tahoma, sans-serif fallbacks)  
**Label/Mono Font:** IBM Plex Mono (with Consolas, monospace fallback)

**Character:** The Thai-first sans is compact, direct, and administrative without feeling bureaucratic. Monospace is restricted to input, output, line gutters, and terse technical badges so data remains visually distinct from interface language.

### Hierarchy
- **Headline:** Bold and compact; used for the workspace title only.
- **Title:** Bold with slightly tightened tracking; used for panel headings and primary empty-state messages.
- **Body:** Regular-weight interface copy with an open reading rhythm.
- **Label:** Semibold compact text for controls, statuses, helper lines, and metadata.
- **Code:** Regular monospace with a fixed roomy line rhythm for source and protected text.

### Named Rules

**The Two-Language Rule.** Thai leads all task instructions; short English identifiers such as INPUT, PROTECTED, and MASK may remain when they improve technical scanning.

**The Monospace Boundary Rule.** Monospace belongs to user data and technical identifiers, never general navigation or explanatory prose.

## Layout

The workspace uses a centered fluid shell capped at 1600px. On wide screens it is a four-part grid: a 248px rule rail, flexible source editor, 44px transformation bridge, and flexible protected editor, with 14px gaps and a minimum working height of 615px. The two editors carry equal visual weight.

Below 1180px, the rules become a five-column strip above the paired editors. At 760px and below, the whole workflow becomes a vertical sequence: actions, rules, source, horizontal bridge, protected result, then legend. Outer padding contracts from fluid desktop spacing to 12px while controls preserve touch-sized height. Mobile does not hide task-critical states; it changes their order and density.

**The Single-Viewport Story Rule.** At desktop presentation widths, rule choice, source, transformation, and protected output must remain simultaneously scannable.

## Elevation & Depth

Depth is hybrid but restrained. One-pixel blue-gray borders perform most structural work; soft ambient shadow belongs primarily to editor panels, the bridge control, primary action, and transient confirmation. Tonal washes communicate state without lifting every surface.

### Shadow Vocabulary
- **Workspace Ambient** (`0 14px 34px rgb(24 53 87 / 7%)`): Softly separates the two primary editors from the canvas.
- **Action Ambient** (`0 7px 18px rgb(8 127 157 / 18%)`): Supports the primary action at rest; hover increases gently.
- **Bridge Structural** (`0 7px 18px rgb(24 53 87 / 10%)`): Keeps the transformation node legible over its connecting rule.
- **Transient Confirmation** (`0 8px 20px rgb(10 35 73 / 18%)`): Reserved for short-lived copy feedback.

### Named Rules

**The Border-First Rule.** Establish hierarchy with surface tone and fine rules before adding shadow.

**The Ambient Ceiling Rule.** Shadows remain cool, diffuse, and below 24% opacity; no glow, glass, or dramatic floating layers.

## Shapes

The form language uses gently curved rectangles and compact circles. Major panels use a restrained 12px radius; actions and icon fields use 8-10px; badges and highlights use 4-7px. Pill geometry is reserved for binary switches and circular geometry for status dots and the transformation node. One-pixel borders stay visible on light surfaces.

**The Quiet Corner Rule.** Rounded forms should soften an official workspace, not make it playful; avoid oversized capsules and nested rounding.

## Components

### Buttons
- **Shape:** Compact rounded rectangle with a 44px minimum height and 10px radius.
- **Primary:** White text on Workbench Teal with a small shield icon and restrained ambient shadow.
- **Hover / Focus:** Hover deepens teal and rises by 1px; focus uses a visible blue 3px translucent outline with 2px offset; active returns to rest position.
- **Secondary:** Navy on white with a strong blue-gray border and soft-surface hover.

### Chips
- **Style:** Quiet neutral chip with compact label, count, and a 7px category dot; rounded to 7px.
- **State:** Color identifies category only; the chip body remains neutral.

### Cards / Containers
- **Corner Style:** Gently curved major panels.
- **Background:** White work surfaces over Cool Canvas; editor interiors use near-white tonal separation.
- **Shadow Strategy:** Editor panels receive Workspace Ambient; rules and legend remain border-defined.
- **Border:** One-pixel Fine Rule.
- **Internal Padding:** Compact 14-18px edges, increasing only for centered empty states.

### Inputs / Fields
- **Style:** Borderless code editor inside a bordered panel, paired with a line-number gutter and fixed monospace rhythm.
- **Focus:** White surface shift plus an inset blue focus definition.
- **Error / Disabled:** Errors use Alert Crimson on a pale crimson wash; disabled primary actions preserve identity and lower opacity.

### Navigation
- **Style:** A slim white product bar with a teal-on-wash shield mark, bold navy name, restrained promise, no-storage state, and outlined GitHub action. On mobile, the promise and privacy label collapse while the brand and GitHub icon remain.

### Rule Toggle
- **Style:** A full-row label combines a soft category icon field, Thai label, short matching clue, and category-colored switch.
- **State:** Hover changes only the neutral row surface; checked state colors the switch, and keyboard focus outlines the whole row.

### Transformation Bridge
- **Style:** A fine structural line passes behind a circular arrow node with a small monospace MASK label.
- **Responsive behavior:** Vertical between editors on desktop; horizontal with the arrow rotated downward on mobile.

## Do's and Don'ts

### Do:
- **Do** keep source and protected output equally prominent and visibly connected.
- **Do** use fine rules and alignment as the primary organizing devices.
- **Do** reserve teal for the primary action and truthful workflow or privacy signals.
- **Do** keep all five rule categories continuously scannable, including on mobile.
- **Do** preserve clear focus states, keyboard operation, and reduced-motion behavior.

### Don't:
- **Don't** turn the interface into a theatrical cyber dashboard.
- **Don't** use decorative glow, glassmorphism, dense gradients, or excessive ornament.
- **Don't** spread category colors across large surfaces or primary actions.
- **Don't** imply storage, fabricated metrics, generated administrator identity, or unsupported masking capabilities.
- **Don't** allow responsive layouts to obscure the before-and-after workflow.
