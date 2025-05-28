#!/bin/bash

#SBATCH --job-name=Explore_Parameters   # MODIFY with your job name
#SBATCH -o logs/%j.out     # Output log
#SBATCH -e logs/%j.err     # Error log
#SBATCH --partition=short # MODIFY with the partition you want to use
#SBATCH --account=t3
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --mem=12000M    # MODIFY with memory needed
#SBATCH --time=00-01:00     # MODIFY with time needed (DD-HH:MM)

# Access SLURM environment variable in Bash
job_id=$SLURM_JOB_ID

# Set paths and filenames
path_to_cards="/work/$USER/Delphes/explore_parameters/LJP/pythia_cards" # MODIFY with your path to your cards 
card="SVJL_nevents-1000_lambdaHV-5_Nc-3_Nf-2_mPioverLambda-1.6_mZprime-3000_rinv-0.3_probvector-0.75_A-Democratic.cmnd"  # MODIFY with your chosen card name

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
output_dir="/work/$USER/Delphes/explore_parameters/LJP/simulations_result/$fname/$(date +%d-%m-%H:%M_$job_id)"

# Create output directory if it doesn't exist

mkdir -p ${output_dir}

source $(conda info --base)/etc/profile.d/conda.sh
conda activate root_tears # MODIFY with your environement containing root

export output_dir=${output_dir}

# Environment variables for Pythia
export PYTHIA8=/work/$USER/pythia8311 # MODIFY with your pythia installation path
export PYTHIA8DATA=$PYTHIA8/share/Pythia8/xmldoc/
export PYTHONPATH=$PYTHIA8/lib:$PYTHONPATH
export LD_LIBRARY_PATH=$PYTHIA8/lib:$LD_LIBRARY_PATH

# Output directory setup
echo "Card path: ${path_to_cards}/${card}"
echo "Output path: ${output_dir}/${rootFile}"

cd /work/$USER/Delphes

# Run DelphesPythia8 simulation
./DelphesPythia8 /work/$USER/Delphes/cards/delphes_card_CMS_HV_filtered.tcl ${path_to_cards}/${card} ${output_dir}/simulation.root > ${output_dir}/simulation_log.txt

# File size check and processing
ls ${output_dir}
du -sh ${output_dir}/${rootFile}

# ROOT clustering->declustering->extraction of data for LJP
echo "Running ROOT post-processing..."
root -b -q "process_to_json.C(\"${output_dir}/simulation.root\", \"${output_dir}\")"

#Plotting Lund Jet plane
echo "Running Python post-processing..."

cd explore_parameters/LJP/Utils/

python3 ljp_plot.py --file ${output_dir}/jets_Scan.json  --outFile ${output_dir}/LJP_plot.png --npxl 50 # MODIFY values if necessary

echo "Job complete."
