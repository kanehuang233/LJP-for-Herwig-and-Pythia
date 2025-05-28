import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
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

    for jet in jet_data:
        for declustering in jet:
            Delta = declustering["Delta"]
            kt = declustering["kt"]

            if Delta > 0 and kt > 0:  # Ensure valid values
                ln_delta_inv.append(np.log(1.0 / Delta))
                ln_kt.append(np.log(kt))

    num_jets = len(jet_data) if jet_data else 1  # Avoid division by zero

    # Define fixed x and y ranges
    x_range = (0, 10)  # ln(1/Delta)
    y_range = (-10, 7)  # ln(kt)

    # Compute 2D histogram (normalized density)
    hist, xedges, yedges = np.histogram2d(ln_delta_inv, ln_kt, bins=100, range=[x_range, y_range])
    hist_normalized = hist / num_jets  # Normalize by total jets

    return hist_normalized, xedges, yedges

# Load and process both files
hist1, xedges, yedges = process_lund_json(args.file1)
hist2, _, _ = process_lund_json(args.file2)

# Compute difference (hist1 - hist2)
diff_hist = hist1 - hist2

# Mask zero-density areas to make them white
diff_hist_masked = np.ma.masked_where((hist1 == 0) & (hist2 == 0), diff_hist)

# Define colormap: blue (negative), white (zero), red (positive)
cmap = plt.cm.seismic
cmap.set_bad(color="white")  # Set zero-density areas to white

# Plot the difference map
plt.figure(figsize=(8, 6))
plt.pcolormesh(xedges, yedges, diff_hist_masked.T, cmap=cmap, norm=Normalize(vmin=-np.max(np.abs(diff_hist)), vmax=np.max(np.abs(diff_hist))))

# Add color bar
plt.colorbar(label="Difference")

# Labels and title
plt.xlabel(r"$\ln(1/\Delta)$")
plt.ylabel(r"$\ln(k_t)$")
plt.title("Difference, Herwig - Pythia\n decay off, dark hadrons ")

# Save the difference plot
plt.savefig(args.outfile, dpi=300, bbox_inches="tight")
print(f"Difference plot saved to {args.outfile}")