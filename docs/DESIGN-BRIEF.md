# Design brief: buyesimfortravel.com

Concept: the departure board. Europe by rail, border after border, with a plan priced per day. Everything reads like station signage: condensed capitals, a dark board with signal-yellow rows, thin rail lines as dividers.

Palette (hex): paper #EEF0EE, surface #FFFFFF, ink #14202B, board #0E1A24, rail blue #0B5C9E, signal yellow #FFC20E (leader highlight), alert #C9432B, mute #5B6A76, line #D3D9DC, pale blue #DCE9F3.

Fonts: Barlow Condensed (headings, labels, numbers) + IBM Plex Sans (text).

Hero: type C. Centred headline on the dark board; under it a horizontal departure-board strip with the top 5 (rank, provider, score) as rows that scroll horizontally on mobile.

Layout: article column with the table of contents on the LEFT (sticky), narrow; sections separated by a thin rail line with small station dots. Wide pages: single column.

Components: sharp 3px radii, 1.5px ink borders, no soft shadows, hard offset shadow on key cards. Tables: ink header row, zebra, sticky first column. Steps: vertical timeline with station dots. FAQ: single-column accordion with plus sign. Rating: horizontal rows ("platform rows") with a score tile on the left in condensed type and criteria as segmented bars.

Signature visuals (src/visuals.py): route-map (rail-style schematic of a one-country base plus day trip), board-plans (departure board of unlimited plans), cap-meter (daily allowance bars), border-days (timeline of a multi-country route), breakeven (fixed vs unlimited by GB per day), plus per-post cover scenes.

Interactive tool: "Plan finder" (countries on route, daily GB, days) giving a plan-type recommendation.

Logo: a ticket-stub / signal lamp mark: yellow circle (signal) on a dark rounded-square with a rail line crossing it.

Microcopy: buttons "Check the board", "Open plan", labels "Platform 1", "On time", "Departures".
