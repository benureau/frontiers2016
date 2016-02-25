# Research Code

This repository contains the code that was used to run the experiments and to generate the figures of the article
**Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience** by [Fabien C. Y. Benureau](http://fabien.benureau.com) and [Pierre-Yves Oudeyer](http://www.pyoudeyer.com), Frontiers in Robotics and AI, 2016.

All the code is placed under the [Open Science License](http://fabien.benureau.com/openscience.html).

There are several things you may want to do with the code:
* Consult the code
* Interacting with the raw plots
* Reproduce the figures and create new ones
* Reproduce the results

## Consult the code

You can typically do that online, or by cloning the repository. This repository uses git submodules to accurately track the version of the other libraries written by the authors that were used in the experiments. You will need to do:
```
git submodule init
git submodule update
```
at the root of the cloned repository directory to clone the submodule as well.

The code is organized as follows:
* The current repository, `frontiers2016`, contains the configurations of the specific experiments used in the paper, as well as the random seeds and the Python notebooks that were used to produce the figures. All configuration are implemented as `SciConfig` objects from the `scicfg` submodule.
* The `explorers` and `learners` submodules contains the algorithmic implementation of the exploration and learning algorithms used in the paper. `fastlearners` contains optional C++ implementation of the LWLR routines (only used in the *objects* experiments). The `learners` package will automatically use them if `fastlearners` is installed, and defaults to (slower) Python implementations if not.
* The `environments` submodule contains the API for the environments the robots are interacting with, as well as the planar arms implementation. The `dovecot` package contains the environments implementation of the object interaction tasks; it requires numerous non-Python dependencies.
* The `experiments` submodule contains the implementation of the computational job that compute the exploration, tests, and results aggregation. It effectively orchestrate how instances from classes from the `explorers`, `learners` and `environments` packages interact with one another. It is supported by the `clusterjobs` submodule that implements the mechanism for submitting jobs to a cluster, and encoding dependencies between jobs (such as targets tasks depending of source tasks, and tests depending on exploration jobs).

## Interacting with raw plots

Static html versions of the notebooks for each figure are available at [fabien.benureau.com/code/frontiers2016.html](http://fabien.benureau.com/code/frontiers2016.html). This is the easiest way to interact with the graphs, and access their provenance data.

## Reproducing the figures and creating new ones

Figures 3, 4 and 7 can be reproduced by merely running Python notebooks. For other figures you will need to download the data files created by the cluster jobs. Figure 10 and 15 are particularly interesting to reproduce, as they only show one run in the paper. By re-running the notebooks, you can inspect other runs (which are sometimes wildly different from the one in the paper).

### Creating a virtual environment

You should consider installing the code in a Python virtual environment. This ensures that the install scripts, which will install specific versions commonly used module such as `numpy`, do not mess with the rest of your setup.

You can use [`pyenv`](https://github.com/yyuu/pyenv), and its plugin [`pyenv-virtualenv`](https://github.com/yyuu/pyenv-virtualenv) to create the virtual environment. Once those are installed, do:

```
pyenv virtualenv 2.7.11 frontiers2016
pyenv activate frontiers2016
```

### Installing the submodules

Optionally, you can install before proceeding [`geos`](http://trac.osgeo.org/geos/), it speeds up coverage computation, especially when reproducing Figure 7.

Inside the cloned repository, run:
```
./install_planar_arms.sh
```
Note that the `install_planar_arms.sh` script will install the dependencies listed in the `submodules/requirements.txt` file. Those match specifically the version used in our experiments, but may be outdated on your machine. You should relax the versions of those requirements in the file as you see fit.

### Getting the data

The data is available at [fabien.benureau.com/code/frontiers2016.html](http://fabien.benureau.com/code/frontiers2016.html). You should uncompress the `.tar.xz` file at a location of your choosing:

```
tar xfv frontiers2016_data.tar.xz
```

Then, indicate the location via the environment variable `BENUREAU_FRONTIERS2016_DATA`, for instance:
```
export BENUREAU_FRONTIERS2016_DATA="~/reasearch/data/"
```
The `BENUREAU_FRONTIERS2016_DATA` variable should point to the directory where the `frontiers2016` directory is located (i.e. not `"~/reasearch/data/frontiers2016/` but `"~/reasearch/data/`).

Once this is done, you can start Jupyter and run the notebooks located in the `planar_arms/` and `objects/` directory
```
jupyter-notebook .
```

If you did not install the `dovecot` submodule, the provenance functions will fail. This is normal.


## Reproducing results

Reasonable efforts were made to make the reproduction of the results as easy as possible. If you want to reproduce the planar arms experiments of Figure 5 and 6 (Figure 3, 4 and 7 are already reproducible with the previous section), all is already setup if you followed the previous steps.

### Installing the code for the *objects* experiments

If you want to reproduce the *objects* experiments, follow those intruction before continuing.

Those experiments require many different dependencies to be installed. You will need to install [V-REP](http://www.coppeliarobotics.com/downloads.html) (version 3.2.3 was used, make sure you install the python bindings), [eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page), [FLANN](http://www.cs.ubc.ca/research/flann/), [FCL](https://github.com/flexible-collision-library/fcl) and [dmpbbo](https://github.com/stulp/dmpbbo). Some of these dependencies may be non-trivial to install; do not hesitate to contact me if you are encountering difficulties (at fabien.benureau@gmail.com), I have extensive experience on installing those on Linux and OS X systems alike.

If you are on OS X and have homebrew installed, you can run `brew install eigen flann libccd` to install some of those dependencies (`libccd` is a dependency of `FCL`).

Once all this is done, do:
```
./install_objects.sh
```

### Reproducing results


The cluster computation involve extensive computation over repeated runs of the experiments. Figure 5 and 6 share the same data, which can reasonably be computed on a personal computer over a day or two at most. Figures 10 to 20 require, combined, between 1000 and 2000 hours of computation, and should probably be run on a cluster (and figures 18 and 19b need the hardware setup, unfortunately not provided when cloning this repository).

In either case, you need to go to the `figure_5/` directory of `planar_arms/`, or the `cluster/` directory of `objects/`. At this point, you may want to double check that the `BENUREAU_FRONTIERS2016_DATA` variable is pointing to a location where you want data to be generated.

There, choose the figure you want to recompute data for (we choose `fig5_cluster.py` in this example), and do:

```
python fig5_cluster.py -w --hd
```

This will generate the configuration files (`--hd`), and display the jobs list (`-w`), and which are ready to be run. As reuse experiments need to exploit the data of source explorations, some jobs will need other to finish running before being ready to be executed.

Note that the program will automatically detect if the command `qstat` and `qsub` are available, and if they are, will assume it is on a cluster and try to submit jobs to it. You may want to edit the `run.pbs` (Portable Batch System) files available inside the `figure_5/`, and `cluster/` directories to match your configuration.

If you edit any files, you should run `python fig5_cluster.py --hd` again. If `qstat` is not available, python will launch the jobs serially on the current machine.

Then do:

```
python fig5_cluster.py --run
```

You will need to run `python fig5_cluster.py --run` multiple times, as new jobs become ready to execute when other finish and make their data available. If jobs crash for any reasons, they are able to resume from the last checkpoint they made (by default, jobs save their state every 300s). You can check the number of jobs that have finished, are running, ready and waiting by running `python fig5_cluster.py -w -q`.

Please note that the job embeds provenance data in their data files, gathered from the current state of the code at execution. If you don't want the provenance data to flag some of the code as dirty, you should always commit all the code (including submodules) before running jobs. Jobs check the continuity of the provenance data when resuming from a checkpoint. If it has changed, the job will restart from scratch.

Do contact me at fabien.benureau@gmail.com if any difficulties arise while trying to run experiments.
