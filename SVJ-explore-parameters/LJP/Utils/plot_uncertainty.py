import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm
import argparse

# Command-line argument parser
parser = argparse.ArgumentParser(description="Compare two Lund Jet Plane plots")
parser.add_argument("--file1", required=True, help="Path to first input JSON file")
parser.add_argument("--file2", required=True, help="Path to second input JSON file")
parser.add_argument("--outfile", required=True, help="Path to save the output difference plot")
args = parser.parse_args()

# Function to load and process Lund JSON data
def process_lund_json(json_file):
    with open(json_file, "r") as f:
        jet_data = [json.loads(line) for line in f if line.strip()]

    ln_delta_inv, ln_kt = [], []
    i = 0
    for jet in jet_data:
        for declustering in jet:
            Delta = declustering["Delta"]
            kt = declustering["kt"]

            if Delta > 0 and kt > 0:  # Ensure valid values
                ln_delta_inv.append(np.log(1.0 / Delta))
                ln_kt.append(np.log(kt))
                i+=1

    num_jets = len(jet_data)  # Avoid division by zero

    # Define fixed x and y ranges
    x_range = (0,6)  # ln(1/Delta)
    y_range = (-4, 6)  # ln(kt)

    # Compute 2D histogram (normalized density)
    hist, xedges, yedges = np.histogram2d(ln_delta_inv, ln_kt, bins=50, range=[x_range, y_range])
    hist_normalized = hist / num_jets  # Normalize by total jets

    return hist_normalized, xedges, yedges

# Load and process both files
hist1, xedges, yedges = process_lund_json(args.file1)
hist2, _, _ = process_lund_json(args.file2)
with np.errstate(divide="ignore", invalid="ignore"):
    ratio_hist = np.where(hist2 > 0, np.abs(hist1-hist2) / hist2, np.nan)  # Avoid division by zero

# Mask zero-density areas to make them white
#ratio_hist_masked = np.ma.masked_invalid(ratio_hist)

# Define colormap: blue (ratio < 1), white (1), red (ratio > 1)
cmap = plt.cm.Reds
cmap.set_bad(color="white")  # Set undefined areas (zero density) to white

# Plot the ratio map
plt.figure(figsize=(8, 6))
plt.pcolormesh(xedges, yedges, ratio_hist.T, cmap=cmap, norm=LogNorm(vmin=0.1, vmax=10))

# Add color bar
plt.colorbar(label="Uncertainty")

# Labels and title
plt.xlabel(r"$\ln(1/\Delta)$")
plt.ylabel(r"$\ln(k_t)$")
# Compute difference (hist1 - hist2)

plt.title("Uncertainty, Herwig-Pythia / Pythia")

# Save the difference plot
plt.savefig(args.outfile, dpi=300, bbox_inches="tight")
print(f"Difference plot saved to {args.outfile}")