import json
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.colors import LogNorm
import matplotlib.colors as mcolors
import argparse
# Load the JSON file
parser = argparse.ArgumentParser(description="Generate a jet density plot from declustering data")
parser.add_argument("--file", required=True, help="Path to input JSON file")
parser.add_argument("--outfile",type=str, default='lund_image.png')
args = parser.parse_args()

  # Update with the correct path if needed
# User-specified output directory


# Ensure the directory exists


# Set output file name


# Read the JSON data
ln_kt = []
ln_Delta = []


with open(args.file, "r") as f:
    jet_data = [json.loads(line) for line in f if line.strip()]

# Extract relevant data: ln(1/Delta) and ln(kt)
ln_delta_inv = []
ln_kt = []
i = 0

for jet in jet_data:
    for declustering in jet:
        Delta = declustering["Delta"]
        kt = declustering["kt"]

        if Delta > 0 and kt > 0:  # Ensure no log errors
            ln_delta_inv.append(np.log(1.0 / Delta))
            ln_kt.append(np.log(kt))


# Total number of jets for normalization
num_jets = len(jet_data)  # Avoid division by zero

# Create 2D histogram (density plot)
plt.figure(figsize=(8, 6))
hist, xedges, yedges = np.histogram2d(ln_delta_inv, ln_kt, bins=50, range = [(0,8),(-4,6)])

# Normalize by the total number of jets to get density
hist_normalized = hist / num_jets  # Each bin represents the fraction of total jets

# Mask zero-density areas to make them white
hist_masked = np.ma.masked_where(hist_normalized == 0, hist_normalized)

# Define colormap: viridis for non-zero values, white for zeros
cmap = plt.cm.viridis.copy()
cmap.set_bad(color="white")

#discrete map
boundaries = np.arange(0, 0.05, 0.0025)  # 0 to 0.03 in steps of 0.0025
n_bins = len(boundaries) - 1
base_cmap = plt.get_cmap('viridis')
discrete_cmap = mcolors.ListedColormap(base_cmap(np.linspace(0, 1, n_bins)))

# Testing color settings
viridis = plt.cm.get_cmap("viridis", 256)
new_colors = viridis(np.linspace(0, 1, 256))
new_colors[:30] = np.linspace([1, 1, 1, 1], new_colors[30], 30)  # fade from white
whitened_viridis = mcolors.ListedColormap(new_colors)


# Plot the density map
plt.pcolormesh(xedges, yedges, hist_masked.T, cmap=cmap,vmin=0,vmax =0.02)
#with discrete :
#plt.pcolormesh(xedges, yedges, hist_masked.T, cmap=discrete_cmap,vmin=0, vmax=0.05)

# Add color bar
plt.colorbar(label="density")

# Labels and title
plt.xlabel(r"$\ln(1/\Delta)$")
plt.ylabel(r"$\ln(k_t)$")


#title
plt.title("Lund Jet Plane \n Pythia SM shower")
#plt.text(3.5,4,"$a=0.3$, $b=0.8$")
#plt.text(5,3," \n Lambda=10, M=default")



plt.savefig(args.outfile)
print(f"Plot saved to {args.outfile}")

# Show the plot

