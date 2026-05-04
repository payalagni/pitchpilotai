---
name: PitchPilot AI Visual Language
colors:
  surface: '#0d150d'
  surface-dim: '#0d150d'
  surface-bright: '#333b32'
  surface-container-lowest: '#081008'
  surface-container-low: '#151e15'
  surface-container: '#192219'
  surface-container-high: '#242c23'
  surface-container-highest: '#2e372e'
  on-surface: '#dce5d7'
  on-surface-variant: '#bbcbb8'
  inverse-surface: '#dce5d7'
  inverse-on-surface: '#2a3329'
  outline: '#869583'
  outline-variant: '#3c4a3c'
  surface-tint: '#3ce36a'
  primary: '#3fe56c'
  on-primary: '#003912'
  primary-container: '#00c853'
  on-primary-container: '#004c1b'
  inverse-primary: '#006e2a'
  secondary: '#7dffa2'
  on-secondary: '#003918'
  secondary-container: '#05e777'
  on-secondary-container: '#00622e'
  tertiary: '#ffb7ae'
  on-tertiary: '#601410'
  tertiary-container: '#ff8d81'
  on-tertiary-container: '#76251f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#69ff87'
  primary-fixed-dim: '#3ce36a'
  on-primary-fixed: '#002108'
  on-primary-fixed-variant: '#00531e'
  secondary-fixed: '#62ff96'
  secondary-fixed-dim: '#00e475'
  on-secondary-fixed: '#00210b'
  on-secondary-fixed-variant: '#005226'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb4ab'
  on-tertiary-fixed: '#410002'
  on-tertiary-fixed-variant: '#7e2a24'
  background: '#0d150d'
  on-background: '#dce5d7'
  surface-variant: '#2e372e'
typography:
  display:
    fontFamily: Work Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  h1:
    fontFamily: Work Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  h2:
    fontFamily: Work Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Work Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Work Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: Work Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  code:
    fontFamily: monospace
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
  container-margin: 32px
  gutter: 20px
---

## Brand & Style

The design system is engineered for high-stakes investor environments, projecting an aura of intelligence, precision, and institutional reliability. The aesthetic is **High-Fidelity Corporate Modern**, blending the utilitarian clarity of finance terminals with the visionary feel of cutting-edge AI.

The interface prioritizes a "command center" experience. It utilizes a sophisticated dark mode palette to reduce visual fatigue during deep-focus analysis. The emotional response is one of calm confidence—leveraging deep blacks to represent stability and "Success Green" to signal growth, momentum, and operational health. Subliminal "glowing" states suggest a living, breathing intelligence that is constantly processing data in the background.

## Colors

This design system utilizes a tiered monochromatic dark scale punctuated by a singular, high-vibrancy accent.

- **Background & Surfaces:** The primary canvas is a true deep charcoal (`#0A0A0B`), ensuring absolute contrast for the neon accents. Surface containers use a slightly elevated charcoal (`#121214`) to create subtle dimensionality.
- **Success Green:** Used exclusively for primary actions, success states, and progress indicators. It serves as the "heartbeat" of the AI.
- **Neutral Grays:** Text follows a strict hierarchy—Zinc-100 for primary headings, Zinc-400 for body text, and Zinc-600 for decorative borders and disabled states.

## Typography

The typography system relies on **Work Sans** (as a high-fidelity alternative to Google Sans available in this framework) to maintain a clean, SaaS-oriented professional look. 

- **Headlines:** Use tighter letter-spacing and heavier weights to feel authoritative.
- **Body:** Set with generous line heights to ensure readability of dense investment data.
- **Labels:** Small caps are utilized for "Overline" text or category tags to distinguish metadata from content.
- **Numerical Data:** Tabular fonts should be prioritized in data grids to ensure alignment of financial figures.

## Layout & Spacing

This design system employs a **12-column fixed grid** for dashboard views and a **fluid-width system** for conversational AI threads. 

- **The 8px Rhythm:** All spacing between elements must be a multiple of 8px (sm, md, lg). 
- **Card-Based Architecture:** Information is strictly organized into card modules. Cards should have a consistent internal padding of 24px (lg).
- **Sidebar:** A narrow, sleek navigation sidebar (fixed at 240px or 80px collapsed) houses primary navigational nodes.

## Elevation & Depth

Depth is achieved through **Tonal Layering** and **Subtle Inner Glows** rather than heavy drop shadows.

- **Level 0 (Base):** `#0A0A0B` - The foundational background.
- **Level 1 (Cards):** `#121214` - With a 1px solid border of `#27272A`.
- **Level 2 (Active/Hover):** When a card or element is active, it gains a subtle 2px inner-border stroke of `#00C853` and a 15% opacity green outer glow (spread 20px).
- **Overlays:** Modals and tooltips use a semi-transparent blur (Backdrop Filter: blur(12px)) to maintain context while focusing the user's attention.

## Shapes

The shape language is **Rounded**, striking a balance between the friendliness of modern SaaS and the structure of professional finance.

- **Standard Elements:** Buttons and input fields use a `0.5rem` (8px) radius.
- **Large Containers:** Dashboard cards and modals use `1rem` (16px) radius for a softer, premium feel.
- **Indicators:** Progress bars and active status pills use full rounded (pill-shaped) ends.

## Components

### Buttons & Inputs
- **Primary Button:** Solid `#00C853` with black text. On hover, apply a soft green outer glow.
- **Ghost Input:** Transparent background, 1px border (`#27272A`), transitions to a Success Green border on focus.

### Cards
- **The "Pitch Card":** Feature-rich containers with a subtle top-border accent. Cards should include a "Pulse" indicator in the top right corner when the AI is actively analyzing data within that module.

### AI Active States
- **Pulse Animation:** Use a keyframe animation for active AI states. A `2px` circle of Success Green that ripples outward, fading from 40% to 0% opacity.
- **Sleek Navigation:** Sidebar icons should be 20px linear icons with high-contrast active states (changing from Zinc-600 to Success Green).

### Feedback & Progress
- **The "Pilot" Progress Bar:** A thin (4px) progress bar using the Success Green. For indeterminate loading, use a shimmering gradient effect moving from `#00C853` to `#00E676`.
- **Status Pills:** Small, high-contrast badges for "Reviewed," "Risk Detected," or "Investor Ready."