---
name: Acoustic Minimal Tactile
colors:
  surface: '#12131b'
  surface-dim: '#12131b'
  surface-bright: '#383842'
  surface-container-lowest: '#0c0e16'
  surface-container-low: '#1a1b24'
  surface-container: '#1e1f28'
  surface-container-high: '#282933'
  surface-container-highest: '#33343e'
  on-surface: '#e2e1ee'
  on-surface-variant: '#bec8ce'
  inverse-surface: '#e2e1ee'
  inverse-on-surface: '#2f3039'
  outline: '#899298'
  outline-variant: '#3f484e'
  surface-tint: '#7bd1fa'
  primary: '#c5eaff'
  on-primary: '#003547'
  primary-container: '#7dd3fc'
  on-primary-container: '#005b78'
  inverse-primary: '#006686'
  secondary: '#fcb973'
  on-secondary: '#492900'
  secondary-container: '#6c3e00'
  on-secondary-container: '#ecab67'
  tertiary: '#ffdfba'
  on-tertiary: '#452b00'
  tertiary-container: '#febc60'
  on-tertiary-container: '#754b00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#c0e8ff'
  primary-fixed-dim: '#7bd1fa'
  on-primary-fixed: '#001e2b'
  on-primary-fixed-variant: '#004d66'
  secondary-fixed: '#ffdcbd'
  secondary-fixed-dim: '#fcb973'
  on-secondary-fixed: '#2c1600'
  on-secondary-fixed-variant: '#683c00'
  tertiary-fixed: '#ffddb5'
  tertiary-fixed-dim: '#fcba5e'
  on-tertiary-fixed: '#2a1800'
  on-tertiary-fixed-variant: '#633f00'
  background: '#12131b'
  on-background: '#e2e1ee'
  surface-variant: '#33343e'
  canvas-base: '#14151C'
  surface-card: '#1C1D26'
  surface-raised: '#22232E'
  surface-overlay: '#2A2B38'
  accent-cyan: '#7DD3FC'
  accent-peach: '#FDBA74'
  text-primary: '#FFFFFF'
  text-secondary: '#F8FAFC'
  text-muted: '#9496A1'
  text-hint: '#5C5E6C'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '300'
    lineHeight: 52px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '400'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '400'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.06em
  metric-xl:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: '200'
    lineHeight: 60px
    letterSpacing: -0.04em
  metric-sm:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '300'
    lineHeight: 28px
    letterSpacing: -0.02em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1.25rem
  gutter-mobile: 0.75rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

The design system embodies the understated luxury, mechanical poise, and tactile precision of high-end acoustic engineering and architectural computing. It treats digital mobile interfaces as physical, CNC-machined anodized panels—matte, tactile, deliberate, and calm. 

Designed for smart environmental management and audio-spatial ergonomics, the interface communicates immediate system states without sensory fatigue. Every element operates in service of ambient clarity, replacing loud visual competition with low-energy precision, subtle mechanical haptics, and soft optical depths.

The aesthetic fuses **Soft Tactile Neomorphism** with **Architectural Matte Minimalism**:
- Recessed bedplates, milled wells, and extruded interactive controls evoke physical consoles.
- Precision lighting models: Top-edge 1px incident micro-bevels paired with deep bottom-recessed shadows replace arbitrary flat divider lines.
- Emotional tone: Calm, authoritative, industrial, and intensely focused on micro-crafted material fidelity.

## Colors

The color palette is calibrated around deep, warm-cast charcoal surfaces reminiscent of dark bead-blasted aluminum. Color is deployed with strict utilitarian restraint: vibrant hues are never used for decorative fills across broad surfaces, but are reserved exclusively for active states, slider level fills, kinetic indicator points, and glowing optical focus rings.

### Surface Hierarchy
- **Canvas Base (`#14151C`):** The foundational recessed substrate absorbing light across full viewport frames.
- **Card Surface (`#1C1D26`):** The primary structural plate for control blocks and grouped telemetry tiles.
- **Raised Controls (`#22232E`):** Distinct interactive physical layers, resting knobs, and inactive toggle thumbs.
- **Overlay & Highlight Surface (`#2A2B38`):** Elevated modals, contextual bottom sheets, and pressed hardware plates.

### Signature Radiant Accent
- **Gradient Transition:** A continuous linear gradient shifting from Icy Blue (`#7DD3FC`) to Warm Peach (`#FDBA74`). Used exclusively to signify active power states, dynamic volume or temperature fills, glowing needle tips, and touch focus states.

### Contrast & Typographic Readability
- **Primary Text (`#FFFFFF`):** High-contrast optic white for key readouts, room identifiers, and primary headings.
- **High-Contrast Labels (`#F8FAFC`):** Crisp secondary white for all interactive controls, input labels, and chip text (guaranteeing minimum 14px accessibility).
- **Muted Supporting Text (`#9496A1`):** Calibrated silver for timestamps, unit badges, and secondary status strings.
- **Hint Text (`#5C5E6C`):** Dedicated exclusively to tertiary guidance, input placeholders, and inactive tick marks.

## Typography

Typography relies entirely on the systematic clarity of **Inter**, structured with deliberate weight shifts to balance ethereal instrumentation readouts with razor-sharp mobile legibility.

### Ergonomic Rules & Hierarchy
- **Strict Size Thresholds:** In compliance with mobile legibility mandates, all interactive UI control labels, pill labels, and button labels have a hard minimum size of `14px` (`label-lg`, `label-md`). Sub-14px typography is restricted exclusively to `12px` (`body-sm`, `label-sm`) and used solely for input hints, inactive track notches, and secondary hardware unit tags.
- **Instrument Readouts (`metric-xl`, `metric-sm`):** Rendered in ultralight weights (`200` to `300`) with tight optical kerning (`-0.04em`). These convey architectural values such as decibels, indoor temperature, and frequency Hertz without visually crowding the layout.
- **System Tags (`label-sm`):** Audio codecs, hardware connection states, and unit measures render in uppercase with deliberate tracking (`0.06em`) to preserve character separation against dark matte surfaces.

## Layout & Spacing

The layout model is governed by thumb-reach ergonomics, prioritizing comfortable one-handed mobile control through intentional bottom-weighted component distribution.

### Grid & Ergonomic Zones
- **Handheld Mobile (< 768px):** 4-column fluid layout with `margin-mobile: 1rem` (16px) and `gutter-mobile: 0.75rem` (12px). Interactive controls, primary sliders, and mode selectors occupy the bottom 60% of the viewport (the natural thumb sweep zone), leaving telemetry dials and status monitors in the upper display zone.
- **Tablet & Wall Terminals (≥ 768px):** 8 to 12-column modular grid with `margin: 2rem` and `gutter: 1.25rem`. Complex radial rings maintain fixed aspect ratios, arranged within symmetrical modular control banks.

### Touch Targets & Spatial Density
- **Minimum Tap Boundaries:** Every interactive element adheres to a strict physical hit-target minimum of **48px × 48px**, regardless of the visual core size of its underlying thumb or icon pin.
- **Hardware Rhythms:** Internal gaps between dial rings, metric pairs, and slider rails align to a baseline 4px/8px rhythm (`space-xs`, `space-sm`), while modular cards and section blocks breathe through generous `space-lg` (24px) and `space-xl` (32px) margins.

## Elevation & Depth

Visual hierarchy is constructed via physical tactile depth rather than high-contrast detached drop shadows. The design mimics physical CNC-carved panels, incorporating subtle extruded edges, light-catching top bevels, and recessed mechanical sockets.

### Tactile Archetypes
1. **Recessed Cavities & Inset Wells:**
   - Dedicated to slider rails, dial perimeter tracks, switch channels, and inactive input fields.
   - Surface: `#14151C`.
   - Shadow model: `box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.7), inset 0 -1px 1px rgba(255, 255, 255, 0.04)`.
   - Optical outcome: The surface appears debossed directly into the matte substrate.

2. **Extruded Tiles & Module Surfaces:**
   - Dedicated to primary control cards and standalone hardware modules.
   - Surface: `#1C1D26` or `#22232E`.
   - Top incident highlight: `box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08)`.
   - Ambient drop depth: `box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.55), 0 4px 10px -2px rgba(0, 0, 0, 0.35)`.
   - Border: `1px solid rgba(255, 255, 255, 0.05)`.

3. **Active Luminescent Glow (Energy States):**
   - Active state switches, engaged sliders, and focused controls discharge an ambient dual-color aura:
   - Glow footprint: `box-shadow: 0 0 20px -2px rgba(125, 211, 252, 0.35), 0 0 32px -4px rgba(253, 186, 116, 0.2)`.

4. **Frosted Translucent Backplates:**
   - Floating navigation rails and contextual quick sheets utilize `backdrop-filter: blur(24px) saturate(140%)` over `#14151C` at 85% opacity, framed with an all-around hairline incident light rim (`rgba(255, 255, 255, 0.08)`).

## Shapes

The shape vocabulary revolves around generous organic curvature combined with mechanical capsule geometry. Pill silhouettes ensure natural thumb targets that guide touch input.

### Curvature Taxonomy
- **Pills (`border-radius: 9999px`):** Used universally for quick-action buttons, interactive filter chips, toggle channels, and slider thumbs.
- **Cards & Control Units (`rounded-xl` to `24px`):** Large surface panels utilize expansive rounded corners, echoing the soft edges of hand-held audio remotes and sculpted wall mounts.
- **Rotary Dials & Indicator Nodes (`border-radius: 50%`):** Perfectly circular forms mimicking machined control wheels.
- **Recessed Inner Wells (`rounded-lg` / `12px` to `16px`):** Text display sockets and structured input wells match the concentric contours of their host containers.

## Components

### Buttons
- **Primary Kinetic Button:** Full pill geometry (`rounded-full`), minimum height `48px`. Surface is filled with the signature linear gradient (`#7DD3FC` to `#FDBA74`). Label is `#14151C` with `label-md` (14px semi-bold). Active press scales to `0.98` with a focused inner shadow (`inset 0 2px 4px rgba(0, 0, 0, 0.35)`).
- **Secondary Tactile Button:** Recessed `#22232E` background, minimum height `48px`, border `1px solid rgba(255, 255, 255, 0.08)`. Top hairline highlight `inset 0 1px 0 rgba(255, 255, 255, 0.12)`. Label is `#FFFFFF` at `14px`.

### Chips & Segmented Selectors
- **Channel Track:** Recessed cavity in `#14151C` with an inner shadow and 4px internal padding.
- **Interactive Chip Item:** Pill capsule (`rounded-full`), minimum touch target `48px` height (or embedded 36px pill within a 48px hit area). Unselected text is `#9496A1` at `14px`.
- **Selected State:** Shifts to elevated `#2A2B38` with an incident top bevel `inset 0 1px 0 rgba(255, 255, 255, 0.15)` and crisp `#FFFFFF` text. Active indicator dots utilize the gradient fill.

### Lists & Navigation Groups
- **List Container:** Clean separated modules on `#1C1D26` surface plates.
- **Row Architecture:** 56px minimum row height to maintain thumb clearance. Top and bottom boundaries utilize hairline separation (`rgba(255, 255, 255, 0.04)`).
- **Row Content:** Primary title `#FFFFFF` (`body-md` 14px/16px), auxiliary metadata `#9496A1` (`body-sm` 12px), trailing interactive Chevron or pill badge.

### Checkboxes & Radio Buttons
- **Radio Buttons:** Outer 22px circle housed in a 48px touch boundary. Inactive state features an inset socket `#14151C` with a 1px border `rgba(255, 255, 255, 0.1)`. Selected state activates an inner 10px circular disc filled with the `#7DD3FC` to `#FDBA74` gradient.
- **Checkboxes:** 22px rounded square (`rounded-sm`), debossed in `#14151C`. On active check, transitions to the signature gradient with an optic white `#14151C` check glyph.

### Input Fields
- **Container:** Debossed well `#14151C`, minimum height `52px`, `rounded-lg` (12px), border `1px solid rgba(255, 255, 255, 0.06)`, padding `space-md`.
- **Typographic Treatment:** User value renders in `#FFFFFF` (`body-md` 14px). Static label sits above in `#F8FAFC` (`label-lg` 14px). Contextual hints render in `#5C5E6C` (`body-sm` 12px).
- **Focused State:** 1px border illuminates in `#7DD3FC` with a soft cyan perimeter glow (`box-shadow: 0 0 12px rgba(125, 211, 252, 0.25)`).

### Cards & Control Modules
- **Substrate:** `#1C1D26` plate with `20px` to `24px` corner radii. Outer boundary defined by `1px solid rgba(255, 255, 255, 0.06)` with top incident bevel `inset 0 1px 0 rgba(255, 255, 255, 0.08)`.
- **Inner Padding:** Generous `space-lg` (24px) buffer ensuring controls do not brush tile boundaries.

### Pill Switches & Ergonomic Faders
- **Pill Switch:** 58px wide × 34px tall recessed channel (`#14151C`). Inactive thumb is a 26px disc in `#2A2B38`. Active toggle transitions the background channel to the signature `#7DD3FC` → `#FDBA74` gradient, with the thumb gliding to the right and gaining a soft optical glow.
- **Linear Ergonomic Fader:** 12px recessed track (`inset 0 2px 4px rgba(0,0,0,0.6)`). Traveled progress is rendered in the gradient fill. Thumb is an extruded 32px tactile capsule featuring two engraved mechanical grip ridges.