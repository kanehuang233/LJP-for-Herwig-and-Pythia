# LJP-for-Herwig-and-Pythia
This is code for generating Primary LJP plots from existing ROOT files. An installation of Pythia 8 installation is included. 
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
- ** `/utils/`: contains codes for plotting the primary LJP plots, use will be introduced next
- ** `/process_to_json.c/`: converts a ROOT file into a JSON file that is later used for plotting, selection on particle pid, jet momentum, and other identities can be made here
- ** `/testing_json.c/`: Printing out more information to see if the selection was working (a code for testing)
- **`/macro_launch/card_generator.sh`**: Generates Pythia configuration cards from a list of input parameters.
- **`/macro_launch/multi_execute.py`**: Runs Pythia/Delphes simulations locally, performs clustering and declustering, and plots LJPs for all cards in `/pythia_cards`.
- **`/macro_launch/execute.py`**: Similar to the above but runs for a single card.
- **`/macro_launch/launch.sh`**: Submits a SLURM job script (`.sh` file) for running simulations with Pythia and Delphes (**not tested**).
- **`/macro_launch/logs/`**: Contains output and error logs for each job run.




