# Proposal fixes, 2026-11-12

Final pass on `proposal.pdf` before the 11:59 pm deadline. Every number below was
checked against `data/city_temps.csv`.

To rebuild: run `make_figures.py`, then `make_proposal.py`, from this folder.
They need pandas and matplotlib.

## Numbers checked (no change needed)

| Claim | Data |
|---|---|
| 30 city average, SSP5-8.5, 2090 to 2100 | 5.46, shown as 5.5 |
| Cape Town / Tehran | 3.13 / 7.47, shown as 3.1 / 7.5 |
| Spread of 2.4 times | 2.39 |
| Models disagree by almost as much as the pathways differ | typical city: model spread 3.2, pathway gap 3.9 |
| 28,440 rows, 9 columns | confirmed |

## Fixes

### Write-up (`make_proposal.py`)
1. **Geography claim corrected.** It said "inland and high latitude cities warm
   fastest, and coastal and tropical cities warm least." Reykjavik is high
   latitude but has the second smallest warming (3.9), so the latitude part
   was wrong. It now says: "Cities deep inside large continents, like Tehran,
   Riyadh and Beijing, warm fastest, and many coastal cities, like Singapore,
   Reykjavik and Cape Town, warm least."
2. **Model disagreement now has a concrete example.** Added "In Lima they range
   from 4.1 to 7.2 degrees." This matches the team plan, except the low end is
   4.1, not 4.0 (Lima, SSP5-8.5, 2090 to 2100 average per model).
3. **Team names:** added the missing commas.

### Figure 2: two pathways (`make_figures.py`)
4. The end labels showed the single year 2100 (5.8C), which disagreed with the
   5.5 in the write-up. The labels now show the 2090 to 2100 average (5.5C and
   1.5C), with a shaded bar over 2090 to 2100 and a subtitle saying so.

### Figure 3: world map
5. The map used the single year 2095, so its labels disagreed with Figure 1
   (San Diego 4.8 vs 4.4, Cape Town 3.4 vs 3.1, Anchorage 7.0 vs 7.2). It now
   uses the same 2090 to 2100 average as Figure 1, and the title says so.
   Caption and list entry updated.

### Figure 4: model disagreement
6. City changed from **San Diego to Lima**, to match the story in the team plan.
7. X axis ended at 2150, leaving a third of the chart empty. It now ends at 2100.
8. Removed the legend, which repeated the line end labels.
9. Subtitle now gives the range: "2090 to 2100 average ranges from 4.1 to 7.2C
   across models." Caption and list entry updated to name Lima.

### Fonts (both scripts)
10. Rebuilding on macOS dropped all bold titles and headings: matplotlib finds
    the regular Helvetica Neue font but not its bold. Arial is now first in
    the font list, so bold renders. The fallback order is otherwise unchanged.

## Not changed

- Figures 1, 5 and 6: already correct and consistent.
- `README.md` still says "Team: TBD". Worth filling in before the prototype.
- No changes to the website (`index.html`, `main.js`, `style.css`).
