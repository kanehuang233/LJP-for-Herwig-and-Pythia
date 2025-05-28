#!/bin/bash

# Set paths and filenames
path_to_cards="/work/$USER/Delphes/explore_parameters/LJP/pythia_cards"  # MODIFY with your path to your cards
output_base_dir="/work/$USER/Delphes/explore_parameters/LJP/simulations_result"

# Loop over each card file in the directory
for card in ${path_to_cards}/*.cmnd; do

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
    fname="lambdaHV-${lambdaHV}_nevents-${nevents}_Nc-${Nc}_Nf-${Nf}_mPioverLambda-${mPioverLambda}_mZprime-${mZprime}_rinv-${rinv}_probvector-${probvector}"
    output_dir="${output_base_dir}/${fname}/$(date +%d-%m-%H:%M)"

    # Create output directory if it doesn't exist
    mkdir -p ${output_dir}

    # Output directory setup
    echo "Processing card: ${card}"
    echo "Output path: ${output_dir}"

    # Change directory to Delphes
    cd /work/$USER/Delphes

    # Run DelphesPythia8 simulation
    echo "Running DelphesPythia8 simulation for card: ${card}..."
    ./DelphesPythia8 /work/$USER/Delphes/cards/delphes_card_CMS_HV_filtered.tcl ${card} ${output_dir}/simulation.root > ${output_dir}/simulation_log.txt

    # Check if the file was created and show file size
    echo "Checking output files..."
    ls ${output_dir}
    du -sh ${output_dir}/simulation.root

    # ROOT clustering->declustering->extraction of data for LJP
    echo "Running ROOT post-processing..."

    root -b -q "process_to_json.C(\"${output_dir}/simulation.root\", \"${output_dir}\")"

    # Plotting Lund Jet plane
    echo "Running Python post-processing..."

    cd explore_parameters/LJP/Utils/
    python3 ljp_plot.py --file ${output_dir}/jets_Scan.json --outFile ${output_dir}/LJP_plot.png --npxl 50 # MODIFY values if necessary

    echo "Job complete for card: ${card}"

done

echo "All jobs complete."
