import os
import subprocess

# Expand the environment variables in the path
path_to_cards = os.path.expandvars("/work/$USER/Delphes/explore_parameters/LJP/pythia_cards")  # Expanding $USER

# List card files
try:
    card_files = os.listdir(path_to_cards)
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Check if the path is correct.")
    exit(1)

# Loop over each card file and create a new Bash script
for card in card_files:
    print(f"Creating job for card: {card}")
    
    # Extract parameters from the card filename using split or regex
    lambdaHV = card.split("lambdaHV-")[1].split("_")[0]
    Nc = card.split("Nc-")[1].split("_")[0]
    Nf = card.split("Nf-")[1].split("_")[0]
    mPioverLambda = card.split("mPioverLambda-")[1].split("_")[0]
    mZprime = card.split("mZprime-")[1].split("_")[0]
    rinv = card.split("rinv-")[1].split("_")[0]
    nevents = card.split("nevents-")[1].split("_")[0]
    probvector = card.split("probvector-")[1].split("_")[0]

    # Set output filename and directory
    fname = f"lambdaHV-{lambdaHV}_nevents-{nevents}_Nc-{Nc}_Nf-{Nf}_mPioverLambda-{mPioverLambda}_mZprime-{mZprime}_rinv-{rinv}_probvector-{probvector}"
    output_dir = f"/work/$USER/Delphes/explore_parameters/LJP/simulations_result/{fname}/$(date +%d-%m-%H:%M_$SLURM_JOB_ID)"
    
    # Create the SLURM job script
    with open(f"sub_{fname}.sh", "w+") as outFile:
        outFile.write("#!/bin/bash\n")

        outFile.write("#SBATCH --job-name=Scan_Eval_fix_Parameters\n")
        outFile.write("#SBATCH --partition=short\n") #can change by standard for longer job 
        outFile.write("#SBATCH --account=t3\n")
        outFile.write("#SBATCH --nodes=1\n")
        outFile.write("#SBATCH --ntasks=2\n")
        outFile.write("#SBATCH --mem=12000M\n")
        outFile.write("#SBATCH --time=00-12:00 \n")

        # Temporary directories and environment setup
        outFile.write("mkdir -p /scratch/$USER/$SLURM_JOB_ID\n")
        outFile.write("export TMPDIR=/scratch/$USER/$SLURM_JOB_ID\n")

        outFile.write("export PYTHIA8=/work/$USER/pythia8311\n")
        outFile.write("export PYTHIA8DATA=$PYTHIA8/share/Pythia8/xmldoc/\n")
        outFile.write("export PYTHONPATH=$PYTHIA8/lib:$PYTHONPATH\n")
        outFile.write("export LD_LIBRARY_PATH=$PYTHIA8/lib:$LD_LIBRARY_PATH\n")

        outFile.write("export output_dir=/scratch/$USER/${SLURM_JOB_ID}\n")
        outFile.write(f"echo \"Card path: {path_to_cards}/{card}\"\n")
        outFile.write(f"echo \"Output path: ${{output_dir}}/{fname}\"\n")
        
        # Job execution commands
        outFile.write(f"mkdir -p {output_dir}\n")

        outFile.write(f"echo \"Card path: {path_to_cards}/{card}\"\n")
        outFile.write(f"echo \"Output path: ${{output_dir}}/{fname}\"\n")

        outFile.write(f"cd /work/$USER/Delphes\n")
        outFile.write(f"./DelphesPythia8 /work/$USER/Delphes/cards/delphes_card_CMS_HV_filtered.tcl {path_to_cards}/{card} {output_dir}/simulation.root > {output_dir}/simulation_log.txt\n")
        
        # File size check and processing
        outFile.write(f"ls {output_dir}\n")
        outFile.write(f"du -sh {output_dir}/simulation.root\n")

        # ROOT post-processing
        outFile.write(f"echo \"Running ROOT post-processing...\"\n")
        outFile.write(f"root -b -q \"process_to_json.C(\\\"{output_dir}/simulation.root\\\", \\\"{output_dir}\\\")\"\n")

        # Python post-processing
        outFile.write(f"echo \"Running Python post-processing...\"\n")
        outFile.write(f"cd explore_parameters/LJP/Utils/\n")
        outFile.write(f"python3 ljp_plot.py --file {output_dir}/jets_Scan.json --outFile {output_dir}/LJP_plot.png --npxl 50\n")

        outFile.write(f"echo \"Job complete.\"\n")

    # Run the job dynamically using sbatch
    try:
        subprocess.run(
            ["sbatch", f"sub_{fname}.sh"],
            check=True
        )
        print(f"Job for {card} submitted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to submit job for {card}: {e}")
