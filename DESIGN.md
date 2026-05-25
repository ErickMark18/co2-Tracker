---
name: CO2 Tracker
description: Carbon footprint dashboard for GitHub Actions deployments
colors:
  primary: "#22c55e"
  primary-muted: "#16a34a"
  accent-green-bright: "#22c55e"
  accent-yellow: "#ca8a04"
  accent-red: "#dc2626"
  accent-blue: "#2563eb"
  bg-primary: "#09090b"
  bg-secondary: "#18181b"
  bg-card: "#1f1f23"
  bg-card-hover: "#27272c"
  text-primary: "#fafafa"
  text-secondary: "#a1a1aa"
  text-muted: "#52525b"
  border-color: "#27272a"
typography:
  display:
    fontFamily: "Space Grotesk, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 700
    lineHeight: 1.1
  body:
    fontFamily: "Space Grotesk, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "0.875rem"
    fontWeight: 500
rounded:
  sm: "8px"
  md: "12px"
  lg: "6px"
spacing:
  sm: "0.5rem"
  md: "1rem"
  lg: "1.5rem"
  xl: "2rem"
---

# Design System: CO2 Tracker

## 1. Overview

**Creative North Star: "The Quiet Instrument"**

A data-forward dashboard that feels like a well-configured terminal: dark, calm, monospaced precision. The interface steps back so the numbers speak. Every element earns its place by displaying or organizing data; decorative chrome is removed unless it aids comprehension.

This is a developer tool for developers who care about sustainability. Not a greenwashing landing page, not an AI dashboard with gradient meshes. It looks like something a technical team would build for themselves: restrained, honest, focused on the metric that matters.

**Key Characteristics:**
- Dark zinc background with forest-green primary accent
- Monospace numbers for scannable data
- Staggered entrance animations that clarify hierarchy, never decorate
- Hover states that lift subtly without announcing themselves
- Zero illustrations; empty states are text-only

## 2. Colors: The Deep Canopy Palette

The system draws from the visual language of a dense forest at dusk: deep shadows, cool dark backgrounds, and isolated bright green points of light. Not a neon sign, not a glowing terminal. A quiet instrument.

### Primary
- **Deep Canopy Green** (#22c55e): The signature accent. Used sparingly on values that matter most (total CO2, best region, positive trends). Never used decoratively. Its rarity is the point.
- **Muted Forest** (#16a34a): Subdued companion for secondary green contexts (hover states, gradient bases).

### Semantic
- **Amber Caution** (#ca8a04): CO2 values in the 50-200g warning range.
- **Alert Red** (#dc2626): CO2 values above 200g, high-emission regions.

### Neutral
- **Near Black** (#09090b): The canvas. Not pure #000; subtle warm tint.
- **Zinc Shadow** (#18181b): Elevated surfaces, secondary containers.
- **Card Surface** (#1f1f23): Primary card backgrounds.
- **Card Hover** (#27272c): Interactive lift on hover.
- **Border Ash** (#27272a): Subtle borders, dividers.
- **Faint Text** (#52525b): Labels, timestamps, metadata.
- **Muted Text** (#71717a): Secondary labels.
- **Secondary Text** (#a1a1aa): Body text, descriptions.
- **Primary Text** (#fafafa): Headlines, key values.

### Named Rules
**The Restrained Green Rule.** The primary accent appears on ≤10% of any given screen. Green text on green backgrounds is forbidden. When green appears, the surrounding context is zinc-dark. The contrast is the message.

## 3. Typography

**Character:** Technical without being cold. Space Grotesk brings geometric clarity with subtle warmth. JetBrains Mono makes numbers feel measured and precise.

### Font Stack
- **Display/Body:** Space Grotesk (with -apple-system, BlinkMacSystemFont fallbacks)
- **Data/Mono:** JetBrains Mono

### Scale
- **Stat Value** (700, 1.875rem): The hero number. Large enough to read across a room. Used for CO2 totals, savings percentages.
- **Card Title** (600, 0.8rem): Uppercase, 0.06em letter-spacing. Section headers that need quick scanning.
- **Body** (400, 0.875rem): Primary content. 1.5 line-height for readability.
- **Label** (500, 0.7rem): Uppercase labels on stats. Small, dense, but legible.
- **Mono Data** (500, 0.8rem): All numeric data values. Consistency makes scanning faster.

### Named Rules
**The Mono-Data Rule.** Every numeric value that a user might compare, sort, or scan is rendered in JetBrains Mono. Dates, CO2 grams, percentages, region codes. Body text remains in Space Grotesk.

## 4. Elevation

**Hover Lift Philosophy.** Surfaces are flat at rest. Shadows appear only as a response to hover state, creating a subtle lift effect. No ambient shadows, no deep card elevations. The hierarchy comes from background tonal shifts (bg-secondary → bg-card → bg-card-hover), not shadow depth.

### Shadow Vocabulary
None at rest. Shadow vocabulary is intentionally empty.

### Hover Behavior
- **Card:** Background shifts from bg-card to bg-card-hover; border-color lightens slightly; subtle box-shadow (0 8px 24px rgba(0,0,0,0.3)) fades in.
- **Ranking Items:** translateX(4px) translate, not shadow. Movement signals interactivity.
- **Stat Cards:** Same treatment as cards.

### Named Rules
**The Flat-By-Default Rule.** No shadows at rest. No border-radius excess. Elevation comes from tonal contrast and motion, not artificial depth.

## 5. Components

### Stat Card
- **Corner Style:** 12px radius
- **Background:** bg-card (#1f1f23)
- **Border:** 1px solid border-color (#27272a)
- **Internal Padding:** 1.25rem 1.5rem
- **Hover:** background → bg-card-hover, border-color → #3f3f46, box-shadow appears
- **Label Style:** 0.7rem uppercase, 0.08em letter-spacing, text-muted color
- **Value Style:** JetBrains Mono, 1.875rem, 700 weight

### Chart Card
- **Corner Style:** 12px radius
- **Background:** bg-card
- **Border:** 1px solid border-color
- **Internal Padding:** 1.5rem
- **Chart Area:** 280px fixed height, responsive width
- **Empty State:** Centered text + relevant icon (chart with no data line)

### Ranking Item
- **Corner Style:** 8px radius
- **Background:** bg-secondary (#18181b)
- **Internal Padding:** 0.875rem 1rem
- **Hover:** background → bg-card-hover, translateX(4px)
- **Position Number:** JetBrains Mono, 0.7rem, muted color, 24px width
- **Repo Name:** Space Grotesk, 0.875rem, primary text, ellipsis overflow
- **Value:** JetBrains Mono, 0.8rem, secondary text

### Alternative Region Card
- **Corner Style:** 12px radius
- **Background:** Linear gradient (rgba(22,163,74,0.08) → bg-card)
- **Border:** 1px solid rgba(22,197,94,0.2)
- **Title Color:** accent-green-bright

### Logo Icon
- **Shape:** 40×40px, 10px radius
- **Background:** Linear gradient (accent-green-bright → accent-muted)
- **Shadow:** 0 4px 12px rgba(34,197,94,0.25)
- **Icon:** 22×22px stroke icon (sun/circle motif)

## 6. Do's and Don'ts

### Do:
- **Do** use monospace for all numeric data values (JetBrains Mono).
- **Do** keep the primary green accent under 10% of any screen area.
- **Do** use entrance animations with staggered delays (0.1s increments) for visual hierarchy.
- **Do** use ease-out-quart or ease-out-quint for all transitions.
- **Do** include direct value tooltips on charts, not just color encoding.
- **Do** respect prefers-reduced-motion by disabling all animations.

### Don't:
- **Don't** use gradient meshes or AI-style decorative backgrounds.
- **Don't** use neon greens (#00ff00), electric blues, or purple plasma effects. The palette stays zinc-dark with isolated green points.
- **Don't** use the "hero metric card" pattern (big number + small label + gradient background) that's common in SaaS analytics.
- **Don't** use cute illustrations or mascots in empty states. Text-only messages.
- **Don't** use border-left as a colored stripe accent on cards or list items.
- **Don't** use bounce or elastic easing curves; they feel dated.
- **Don't** animate layout properties (width, height, top, left, margins).
- **Don't** use pure #000 or #fff. Tint every neutral toward the brand hue.