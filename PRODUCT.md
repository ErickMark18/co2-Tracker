# Product

## Register

product

## Users

Developers and DevOps engineers who deploy code via GitHub Actions. They work in terminals and IDEs, monitor CI/CD pipelines, and care about efficiency. The context is observational: after a deployment, they check the dashboard to understand impact. Primary job: see carbon footprint at a glance and identify optimization opportunities.

## Product Purpose

CO2 Tracker quantifies and visualizes the carbon footprint of CI/CD deployments. It exists because cloud regions vary wildly in carbon intensity, and developers who care about sustainability need a way to see that impact. Success means a developer can look at this tool and immediately understand: "my deployments this week produced X grams of CO2, and if I'd used Stockholm instead of Sydney, I'd have saved Y%."

## Brand Personality

**Verde, Minimalista, Amigable.**
Green as environmental identity but not aggressively "eco" (no leaf icons, no green-washing). Minimal in the developer-tool sense: data-forward, no fluff, monospace fonts for numbers. Friendly in that it explains things clearly without being corporate or preachy. Think: "a helpful colleague who happens to know carbon intensity data."

## Anti-references

- **No AI aesthetics.** No gradient meshes, no neural-network motifs, no "smart" or "magic" language. This is a data tool, not an AI product.
- **No neon on dark.** Avoid cyberpunk greens (#00ff00), electric blues, or purple plasma effects. The palette should feel like a modern terminal, not a gaming rig.
- **No generic SaaS dashboard.** Avoid the "hero metric card" pattern (big number + small label + gradient) that's everywhere in SaaS analytics.
- **No illustration-heavy emptiness.** Empty states should be a clear message, not a cute mascot or stock illustration.

## Design Principles

1. **Data first, chrome second.** Every UI element earns its place by displaying or organizing data. Decorative elements are removed unless they aid comprehension.

2. **Numbers deserve typography.** When the primary content is quantitative, numbers get the same typographic care as headlines. Monospace for data values, clear hierarchy for units.

3. **Motion clarifies, never decorates.** Animations communicate state change (loading, transition, feedback). If an animation doesn't help the user understand what's happening, it's removed.

4. **Reduce cognitive load.** Developers are busy. The dashboard shows what's important immediately: total CO2, trend, worst offender. Progressive disclosure for details.

5. **Accessibility is baseline.** Not a feature add-on. WCAG AA contrast ratios, keyboard navigation, reduced-motion support, and screen-reader-friendly markup are default.

## Accessibility & Inclusion

- **WCAG AA compliance** as minimum standard for contrast ratios
- **`prefers-reduced-motion`** respected: all animations simplified or disabled
- **Keyboard navigation** for all interactive elements
- **Semantic HTML** and ARIA labels for screen readers
- **Color is not the only indicator:** green/yellow/red badge also has text label, charts have direct value tooltips