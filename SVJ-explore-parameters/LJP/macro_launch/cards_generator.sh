#!/bin/bash

# List of values for mass of leptophobic portal Z' # MODIFY
mzprime_values=(3000)

# List of values for invisible fraction # MODIFY
rinv_values=(0.1)

# List of values for lightest dark pseudoscalar mass over LambdaHV # MODIFY
mPiOverLambda_values=(0.5 2)  

# List of values for dark sector confinement scale # MODIFY
lambda_values=(5)

# List of values for number of events # MODIFY
nevents_values=(30000)

# List of values for number of color for dark model # MODIFY (optional)
n_c_values=(3)

# List of values for number of color for dark model # MODIFY (optional)
n_f_values=(2)

# List of values for the prob vector # MODIFY (optional)
probvector_values=(0.75)

# Loop through all combinations of parameters and run the Python script
for mzprime in "${mzprime_values[@]}"; do
    for rinv in "${rinv_values[@]}"; do
        for mPiOverLambda in "${mPiOverLambda_values[@]}"; do
            for lambda_hv in "${lambda_values[@]}"; do
                for n_c in "${n_c_values[@]}"; do
                    for n_f in "${n_f_values[@]}"; do
                        for nevents in "${nevents_values[@]}"; do
                            for probvector in "${probvector_values[@]}"; do
                                # Run the Python script with the corresponding parameters # MODIFY PATHS TO YOURS and desired decays
                                #With hadronic decay
                                python3 /work/$USER/Delphes/explore_parameters/LJP/Utils/svj_helper_hadronic.py --mMediator "$mzprime" --rinv "$rinv"  --mPiOverLambda "$mPiOverLambda" --lambda "$lambda_hv" --Nc "$n_c" --Nf "$n_f" --nevents "$nevents" --probvector "$probvector" --directory /work/ext-cehrhardt/Delphes/explore_parameters/LJP/pythia_cards/
                                #With leptonic + hadronic decay
                                # python3 /work/$USER/Delphes/explore_parameters/LJP/Utils/svjHelper.py --mZprime "$mzprime" --rinv "$rinv"  --mPiOverLambda "$mPiOverLambda" --lambda "$lambda_hv" --Nc "$n_c" --Nf "$n_f" --nevents "$nevents" --probvector "$probvector" --directory /work/ext-cehrhardt/Delphes/explore_parameters/LJP/pythia_cards/
                            done
                        done
                    done
                done
            done
        done
    done
done