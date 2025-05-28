#!/bin/bash

# Set paths and filenames
path_to_cards="/afs/cern.ch/work/k/kan/work/ILC/pythia13" # MODIFY with your path to your cards
card="mymain.cmnd"  # MODIFY with your chosen card name

# Extract parameters from the card filename using sed
lambdaHV=$(echo $card | sed -E 's/.*lambdaHV-([^_]*)_.*/\1/')
Nc=$(echo $card | sed -E 's/.*Nc-([^_]*)_.*/\1/')
Nf=$(echo $card | sed -E 's/.*Nf-([^_]*)_.*/\1/')
mPioverLambda=$(echo $card | sed -E 's/.*mPioverLambda-([^_]*)_.*/\1/')
mZprime=$(echo $card | sed -E 's/.*mZprime-([^_]*)_.*/\1/')
rinv=$(echo $card | sed -E 's/.*rinv-([^_]*)_.*/\1/')
nevents=$(echo $card | sed -E 's/.*nevents-([^_]*).*/\1/')
probvector=$(echo $card | sed -E 's/.*probvector-([^_]*).*/\1/')

# Set output filename and directory
fname="simulation"
output_dir="/afs/cern.ch/work/k/kan/work/ILC/pythia13/default"

# Create output directory if it doesn't exist
mkdir -p ${output_dir}

# Output directory setup
echo "Card path: ${path_to_cards}/${card}"
echo "Output path: ${output_dir}/${rootFile}"

cd /afs/cern.ch/work/k/kan/work/Delphes

# Run DelphesPythia8 simulation
echo "Running DelphesPythia8 simulation..."

./DelphesPythia8 /afs/cern.ch/work/k/kan/work/Delphes/cards/delphes_card_CMS_HV_filtered.tcl ${path_to_cards}/${card} ${output_dir}/simulation.root > ${output_dir}/simulation_log.txt

# Check if the file was created and show file size
echo "Checking output files..."
ls ${output_dir}
du -sh ${output_dir}/simulation.root

