import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "proposal.pdf")

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
SANS = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]

TITLE = "One number, thirty answers"
SUB = "DSC 106 Final Project Proposal"
TEAM = "Team members: Abigail Suwargo Alina Gao Fei Liang"

DATASET = (
    "CMIP6 monthly near surface air temperature (variable tas, table Amon) from the "
    "Pangeo CMIP6 archive on Google Cloud. We sampled the nearest model grid point to "
    "each of 30 cities across 24 countries and averaged to annual means. Four models "
    "(CanESM5, GFDL-ESM4, IPSL-CM6A-LR, MRI-ESM2-0) and three experiments (historical "
    "1950 to 2014, SSP1-2.6 and SSP5-8.5 2015 to 2100). 28,440 rows and 9 columns. Each "
    "city's warming is measured against its own 1981 to 2010 average, so every number "
    "below is local warming, not absolute temperature."
)

WRITEUP = [
    "Climate targets are written as one global number, but nobody lives in a global average.",
    "We want to show what that number hides.",
    "Under the high emissions pathway, the thirty cities in our data warm by 5.5 degrees on average by the end of the century.",
    "Inside that one average, Cape Town warms 3.1 degrees and Tehran warms 7.5. That is a spread of 2.4 times.",
    "The pattern is not random. Inland and high latitude cities warm fastest, and coastal and tropical cities warm least.",
    "There is a second layer of uncertainty on top of that.",
    "For a single city on a single pathway, the four models disagree by almost as much as the two pathways differ from each other.",
    "Our explorable explanation walks the reader from the global number down to one city, then shows the model spread behind that city's number.",
    "The main interaction is a world map with a year slider and a pathway toggle. Clicking a city pins it and the charts below update to that city.",
    "The takeaway is that a global average is a budget, not a forecast for a place.",
]

SHORT = [
    "End of century warming for all 30 cities under SSP5-8.5, ranked.",
    "Mean warming across the 30 cities on both pathways, 1950 to 2100.",
    "The same warming shown geographically for a single year.",
    "One city, one pathway, four models, showing the disagreement.",
    "How much warming each city avoids on the low emissions pathway.",
    "Six representative cities on both pathways, on a shared scale.",
]

CAPTIONS = [
    ("fig1_city_ranking.png",
     "Figure 1. End of century warming for all 30 cities under SSP5-8.5, averaged over the four models. This is the hook for the article."),
    ("fig2_pathways.png",
     "Figure 2. Mean warming across the 30 cities. History to 2014, then the two pathways. This establishes the shared ground before the article complicates it."),
    ("fig3_world_map.png",
     "Figure 3. The same warming shown geographically for a single year. In the article this becomes the main interactive view, with a year slider and a pathway toggle."),
    ("fig4_model_spread.png",
     "Figure 4. One city, one pathway, four models. The direction is settled and the size is not. This is the second layer of the story."),
    ("fig5_pathway_choice.png",
     "Figure 5. How much warming each city avoids on the low emissions pathway, sorted by the size of the gap. Riyadh avoids 5.5 degrees and Cape Town avoids 2.3."),
    ("fig6_small_multiples.png",
     "Figure 6. Six representative cities on both pathways, on a shared scale, showing how differently the same two futures land."),
]


def text_page(pdf):
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor("white")
    y = 0.945
    fig.text(0.08, y, TITLE, fontsize=22, fontweight="bold", color=INK, fontfamily=SANS)
    y -= 0.035
    fig.text(0.08, y, SUB, fontsize=11.5, color=INK2, fontfamily=SANS)
    y -= 0.022
    fig.text(0.08, y, TEAM, fontsize=11.5, color=MUTED, fontfamily=SANS)

    y -= 0.055
    fig.text(0.08, y, "Dataset", fontsize=13, fontweight="bold", color=INK, fontfamily=SANS)
    y -= 0.026
    for line in textwrap.wrap(DATASET, 92):
        fig.text(0.08, y, line, fontsize=10.5, color=INK2, fontfamily=SANS)
        y -= 0.0195

    y -= 0.035
    fig.text(0.08, y, "Writeup", fontsize=13, fontweight="bold", color=INK, fontfamily=SANS)
    y -= 0.028
    for para in WRITEUP:
        for line in textwrap.wrap(para, 92):
            fig.text(0.08, y, line, fontsize=10.5, color=INK, fontfamily=SANS)
            y -= 0.0205
        y -= 0.006

    y -= 0.028
    fig.text(0.08, y, "Static visualizations", fontsize=13, fontweight="bold", color=INK, fontfamily=SANS)
    y -= 0.026
    for i, short in enumerate(SHORT, 1):
        for j, line in enumerate(textwrap.wrap(f"{i}. {short}", 92)):
            fig.text(0.08 if j == 0 else 0.095, y, line, fontsize=10.5, color=INK2,
                     fontfamily=SANS)
            y -= 0.0205

    pdf.savefig(fig)
    plt.close(fig)


def figure_page(pdf, name, caption):
    img = mpimg.imread(os.path.join(FIGS, name))
    h, w = img.shape[:2]
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor("white")

    avail_w, avail_h = 0.88, 0.80
    k = (8.5 / 11) * (h / w)
    box_w = min(avail_w, avail_h / k)
    box_h = box_w * k

    ax = fig.add_axes([(1 - box_w) / 2, 0.955 - box_h, box_w, box_h])
    ax.imshow(img)
    ax.axis("off")

    cy = 0.955 - box_h - 0.028
    for line in textwrap.wrap(caption, 95):
        fig.text(0.08, cy, line, fontsize=10, color=INK2, fontfamily=SANS)
        cy -= 0.019

    pdf.savefig(fig)
    plt.close(fig)


with PdfPages(OUT) as pdf:
    text_page(pdf)
    for name, cap in CAPTIONS:
        figure_page(pdf, name, cap)

print("wrote", OUT, os.path.getsize(OUT), "bytes")
