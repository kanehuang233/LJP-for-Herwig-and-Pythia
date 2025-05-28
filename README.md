# LJP-for-Herwig-and-Pythia
This is code for generating Primary LJP plots from existing ROOT files. An installation of Pythia 8 installation is included. It is based on [this](https://github.com/cesarecazzaniga/LJP) and [this](https://github.com/Kla1m/SVJ-explore-parameters).
## Installation:
### Delphes and Pythia8

In order to properly run the code, you need a working installation of [ROOT](https://root.cern). On lxplus this is provedided by default (you can check just typing root on the terminal), if you want to run the code on your laptop, then you need to create an environment with a working ROOT installation. To create an environment you can use [Anaconda](https://docs.anaconda.com/anaconda/install/). Once installed, you can create an enviroment (specify the name you want in ```${name_of_env}```) and install ROOT:

```
conda create --name ${name_of_env} python=3.8

conda activate python=3.8

conda install -c conda-forge root

```

If everything went smoothly, typing ```root``` on the terminal should open the interactive mode of the program. In order to run the following installation, and the MC chain, then you need always to activate your virtual environment with ROOT installation.

We want to install Delphes and have the possibility to run with it also Pythia8. To do this, you need to follow these instructions. First, check the current most updated Pythia8 version [here](https://www.pythia.org), and copy the link of the version. Then, you can get it in your current directory with (xx need to be specified according to the most recent version):

```wget https://www.pythia.org/download/pythia83/pythia83xx.tgz```

Then, run:

```
tar xzvf pythia83xx.tgz
cd pythia83xx
./configure
make install
```

Outside Pythia8 directory, you can then install Delphes (check most updated version [here](https://github.com/delphes/delphes)):

```
git clone https://github.com/delphes/delphes.git Delphes
cd Delphes
```

To run the FastJet plugin for the LJP decomposition using ROOT macros and Delphes libraries, you need to follow these steps:

  1. Create a directory inside ```Delphes/external/fastjet/contribs/``` called ```LundPlugin```.
  2. Copy inside the directory ```LundPlugin``` the following files from the FastJet [LJP plugin](https://github.com/fdreyer/LundPlane): LundGenerator.cc, LundGenerator.hh, LundJSON.hh, LundWithSecondary.cc, LundWithSecondary.hh, SecondaryLund.cc, SecondaryLund.hh
  3. You need to use [this Makefile](https://github.com/cesarecazzaniga/LJP/blob/main/Makefile) (substitute with Delphes default one)  

After these steps, you can just run: ```make```.

Now you need to export Pythia8 path:

```
export PYTHIA8=path_to_PYTHIA8_installation_dir
export PYTHIA8DATA=$PYTHIA8/share/Pythia8/xmldoc/
export PYTHONPATH=$PYTHIA8/lib:$PYTHONPATH
export LD_LIBRARY_PATH=$PYTHIA8/lib:$LD_LIBRARY_PATH
```

Finally, you can install Delphes-Pytha8 interfece (command must be executed inside Delphes directory):

```
make HAS_PYTHIA8=true
```
## Useful tools in this repository:

### '/LJP/': contains tools needed for generating LJP plots.
- **`/utils/`: contains codes for plotting the primary LJP plots, use will be introduced next
- **`/process_to_json.c/`: converts a ROOT file into a JSON file that is later used for plotting, selection on particle pid, jet momentum, and other identities can be made here
- **`/testing_json.c/`: Printing out more information to see if the selection was working (a code for testing)

### `/macro_launch/`: Contain potentially useful code for setting up a workflow, which I did not use
The following were used to generate a pythia sample from given card, I only used execute.sh, but others can be modified to process multiple cards at once, or one can totally run pythia indenpendently and ignore these.
- **`/macro_launch/execute.py`**: generate a ROOT file based on a given card
- **`/macro_launch/card_generator.sh`**: Generates Pythia configuration cards from a list of input parameters.
- **`/macro_launch/multi_execute.py`**: Runs Pythia/Delphes simulations locally, performs clustering and declustering, and plots LJPs for all cards in `/pythia_cards`.
- **`/macro_launch/launch.sh`**: Submits a SLURM job script (`.sh` file) for running simulations with Pythia and Delphes (**not tested**).
- **`/macro_launch/logs/`**: Contains output and error logs for each job run.

## Workflow:
- clone this repository in your Delphes direcotry, move `process_to_json.C` and `testing_json.c` out to the Delphes directory
- To generate a ROOT file using Pythia8, use the `/macro_launch/execute.py` and modify the path to input and output files within it. Alternatively, run Pythia8 independently and get the ROOT file, it is totally fine.
- After you generate a ROOT file, either from Herwig or Pythia, run `root -b -q "process_to_json.C(\"Path_to_ROOT_File", \"Output_directory")"` to generate a json file with information needed for plotting the LJP. Clustering and anti-cluster are performed in this step. One can modify the `process_to_json.C` file to decide whether to include invisible particles, do a selection on jet pt, use a different value for R, etc.
-   You can first use `root -b -q "testing_json.C(\"Path_to_ROOT_File", \"Output_directory")"` to see if your selection on pdgid or other parameter is working properly, as it also saves data for each particle.
## Plotting
- To plot a primary LJP, run `python3 SVJ-explore-parameters/LJP/Utils/plot.py --file Directory_of_INPUT_FILE --outfile Directory_of_OUTPUT_FILE `
- To plot a ratio of LJP's of 2 files, say, File1/file2, run `python3 SVJ-explore-parameters/LJP/Utils/plot_ratio.py --file1 Path_to_JSON_file1 --file2 Path_to_JSON_file2 --outfile OUTPUT_Path`
- To plot uncertainty of ratio, namely, (file1-file2)/file2, run `python3 SVJ-explore-parameters/LJP/Utils/plot_uncertainty.py --file1 Path_to_JSON_file1 --file2 Path_to_JSON_file2 --outfile OUTPUT_Path`

Alternatively, make your own code for plotting



