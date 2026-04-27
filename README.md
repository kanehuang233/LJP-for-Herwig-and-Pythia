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

### `/LJP/`: contains tools needed for generating LJP plots.
- `/utils/`: contains codes for plotting the primary LJP plots, use will be introduced next
- `/process_to_json.c/`: converts a ROOT file into a JSON file that is later used for plotting, selection on particle pid, jet momentum, and other identities can be made here
- `/testing_json.c/`: Printing out more information to see if the selection was working (a code for testing)

### `/macro_launch/`: Contain potentially useful code for setting up a workflow, which I did not use
The following were used to generate a pythia sample from given card, I only used execute.sh, but others can be modified to process multiple cards at once, or one can totally run pythia indenpendently and ignore these.
- **`/macro_launch/execute.py`**: generate a ROOT file based on a given card
- **`/macro_launch/card_generator.sh`**: Generates Pythia configuration cards from a list of input parameters.
- **`/macro_launch/multi_execute.py`**: Runs Pythia/Delphes simulations locally, performs clustering and declustering, and plots LJPs for all cards in `/pythia_cards`.
- **`/macro_launch/launch.sh`**: Submits a SLURM job script (`.sh` file) for running simulations with Pythia and Delphes (**not tested**).
- **`/macro_launch/logs/`**: Contains output and error logs for each job run.


## Installing Herwig 7 with Hidden Valley 

The Herwig Hidden Valley setup used for the Lund Jet Plane comparison was built locally from source.  
The instructions below install a private Python 3.9, Mercurial, Autoconf, and then use `herwig-bootstrap` to build Herwig/ThePEG together with Rivet and YODA.

This example assumes installation under a private AFS directory. Change `PREFIX` to your own working area.

```bash
export PREFIX=<path to your installation directory>

mkdir -p $PREFIX/src/python
cd $PREFIX/src/python
```

### 1. Install a private Python 3.9

```bash
wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz
tar xzf Python-3.9.18.tgz
cd Python-3.9.18

./configure --prefix=$PREFIX --enable-shared --with-pic
make -j8
make install -j8

cd $PREFIX/bin
ln -sf python3.9 python

export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH

pip3 install cython sympy scipy six
```

Check that the local Python is being used:

```bash
which python
python --version
```

### 2. Install Mercurial locally

Herwig/ThePEG development versions are obtained through Mercurial, so a recent local `hg` installation is needed.

```bash
mkdir -p $PREFIX/src/mercurial
cd $PREFIX/src/mercurial

wget https://www.mercurial-scm.org/release/mercurial-6.6.tar.gz
tar xzf mercurial-6.6.tar.gz
cd mercurial-6.6

make local

export PATH=$PREFIX/src/mercurial/mercurial-6.6:$PATH

hg --version
```

### 3. Install Autoconf 2.71 locally

```bash
cd $PREFIX

wget https://ftp.gnu.org/gnu/autoconf/autoconf-2.71.tar.xz
tar -xf autoconf-2.71.tar.xz
cd autoconf-2.71

./configure --prefix=$PWD/local
make
make install

export PATH=$PREFIX/autoconf-2.71/local/bin:$PATH

autoconf --version
```

The version should report `autoconf 2.71`.

### 4. Build Herwig using `herwig-bootstrap`

Return to the installation prefix:

```bash
cd $PREFIX
```

Then run `herwig-bootstrap`. The setup used for this comparison built Herwig and ThePEG from their Mercurial development versions:

```bash
./herwig-bootstrap $PWD \
  --rivet-version=4.0.1 \
  --yoda-version=2.0.1 \
  --herwig-hg \
  --thepeg-hg \
  --thepeg-version="default" \
  --herwig-version="default"
```

If the Pythia8 interface is not needed, build without `TheP8I`:

```bash
./herwig-bootstrap $PWD \
  --rivet-version=4.0.1 \
  --yoda-version=2.0.1 \
  --herwig-hg \
  --thepeg-hg \
  --thepeg-version="default" \
  --herwig-version="default" \
  --without-thep8i
```

### 5. Environment setup after installation

For later sessions, the following environment variables should be set before running Herwig:

```bash
export PREFIX=<path to your installation directory>
export PATH=$PREFIX/bin:$PREFIX/src/mercurial/mercurial-6.6:$PREFIX/autoconf-2.71/local/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH
```

## ROOT File Generation

** For Python, simply use `/macro_launch/execute.py`, a sample command card can be found [here](https://github.com/kanehuang233/LJP-for-Herwig-and-Pythia/blob/main/SVJ-explore-parameters/mymain.cmnd), one can alter the parameters in the study if interested.
** For Herwig, a set of sample configs can be found [here](https://github.com/kanehuang233/LJP-for-Herwig-and-Pythia/tree/main/default).
- *** In your directory of the configs, run `Herwig read LHC-HiddenValley.in`, this generate a `.run` file which can be used to run the Herwig simulation
- *** After generating the `.run` file, edit the lines:
  ```text
  PrintEvent
  <number of events you want>
  ```
  and run `Herwig run LHC-HiddenValley.run -N <number of events>`
- *** This generates a `.hepmc` file, convert it to a root file. I used the HepMC plugin in Delphes but there should be better ways of doing it:
```bash
/afs/cern.ch/work/k/kan/work/Delphes2/DelphesHepMC2 /afs/cern.ch/work/k/kan/work/Delphes2/cards/delphes_card_CMS.tcl /afs/cern.ch/work/k/kan/ILC-HiddenValley.root /afs/cern.ch/work/k/kan/work/ILC/default/ILC-HiddenValley.hepmc
```


## ROOT to LJP
The following workflow is run from the Delphes directory, and assumes that the root file is already generated. For the instructions of generating the ROOT file, read below.
- clone this repository in your Delphes direcotry, move `process_to_json.C` and `testing_json.c` out to the Delphes directory
- To generate a ROOT file using Pythia8, use the `/macro_launch/execute.py` and modify the path to input and output files within it. Alternatively, run Pythia8 independently and get the ROOT file, it is totally fine.
- After you generate a ROOT file, either from Herwig or Pythia, run `root -b -q "process_to_json.C(\"Path_to_ROOT_File", \"Output_directory")"` to generate a json file with information needed for plotting the LJP. Clustering and anti-cluster are performed in this step. One can modify the `process_to_json.C` file to decide whether to include invisible particles, do a selection on jet pt, use a different value for R, etc.
    (You can first use `root -b -q "testing_json.C(\"Path_to_ROOT_File", \"Output_directory")"` to see if your selection on pdgid or other parameter is working properly, as it also saves data for each particle.)
## Plotting
- To plot a primary LJP, run `python3 SVJ-explore-parameters/LJP/Utils/plot.py --file Directory_of_INPUT_FILE --outfile Directory_of_OUTPUT_FILE `
- To plot a ratio of LJP's of 2 files, say, File1/file2, run `python3 SVJ-explore-parameters/LJP/Utils/plot_ratio.py --file1 Path_to_JSON_file1 --file2 Path_to_JSON_file2 --outfile OUTPUT_Path`
- To plot uncertainty of ratio, namely, (file1-file2)/file2, run `python3 SVJ-explore-parameters/LJP/Utils/plot_uncertainty.py --file1 Path_to_JSON_file1 --file2 Path_to_JSON_file2 --outfile OUTPUT_Path`

Alternatively, make your own code for plotting

## Step by Step comparison:
The default config assumes a ee collision to remove impact from ISR and MPI
### To turn off SM Hardonization:
  - Herwig: Add the following line to `ILC-HiddenValley.in`, after the section labeled `# Other parameters for run`:
    ```text
    set /Herwig/Decays/DarkQDecayME0:Hadronization No
    ```
  - Pythia: In the `.cmnd` file, add the line:
  ```text
  HadronLevel:Hadronize = off
  ```
### To turn off SM shower:
- Herwig: Add the following line to `ILC-HiddenValley.in`, after the section labeled `# Other parameters for run`:

```text
set /Herwig/Decays/DarkQDecayME0:Shower No
```

- Pythia:

```text
TimeShower:QCDshower = off
```
### To turn off decay to SM:
- Herwig: In `dark_shower_frag.in`, remove or comment out the lines defining the dark rho decays to SM particles. In the current version of the card, these are approximately lines `185–305`.
- Pythia: Remove or comment out the dark rho decay channels to SM quarks, for example:
  ```text
  4900113:addChannel = 1 0.2 91 -1 1
  4900113:addChannel = 1 0.2 91 -2 2
  4900113:addChannel = 1 0.2 91 -3 3
  4900113:addChannel = 1 0.2 91 -4 4
  4900113:addChannel = 1 0.2 91 -5 5
  ```
### To turn off dark hadronization as well:
- Herwig: Add the following line to `ILC-HiddenValley.in`:
```text
set /Herwig/Generators/EventGenerator:EventHandler:HadronizationHandler NULL
```
- Pythia: In the section of `HV Settings`, change the line to:
```text
HiddenValley:fragment = off
```

#### Notes: 
- For Herwig, the `HiddenValley.model` is read by the `.in` file in the run, it is advised to keep a copy of the file in the same directory of `.in` file, and modification can be made to that specific `HiddenValley.model` so that modifications are local.
- Remember to check the `LambdaDark` setting and `PTCutOff`.
- Some other parameters that could results in shift in the LJP includes, for example, for Pythia: `aLund`and `bmqv2`; for Herwig, `ClMaxLight`, `ClSmrLight` and 'PSplitLight'
  


