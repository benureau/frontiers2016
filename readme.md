# Research Code

This repository contains the code that was used to run the experiments and to generate the figures of the article
**Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience** by [Fabien C. Y. Benureau](http://fabien.benureau.com) and [Pierre-Yves Oudeyer](http://www.pyoudeyer.com).

All the code is placed under the [Open Science License](http://fabien.benureau.com/openscience.html).


## Interacting with raw plots

Static html versions of the notebooks for each figure are available at [fabien.benureau.com/code/frontiers2016.html](http://fabien.benureau.com/code/frontiers2016.html). This is the easiest way to interact with the graphs, and access their provenance data.


## Reproducing results

Reasonable efforts were made to make the reproduction of the results as easy as possible.


### Creating a virtual environment

You should consider installing the code in a Python virtual environment. This ensures that the install scripts, which will install specific versions commonly used module such as `numpy`, do not mess with the rest of your setup.

You can use [`pyenv`](https://github.com/yyuu/pyenv), and its plugin [`pyenv-virtualenv`](https://github.com/yyuu/pyenv-virtualenv) to create the virtual environment. Once those are installed, do:

```
pyenv virtualenv 2.7.11 frontiers2016
pyenv activate frontiers2016
```


### Installing the code for the *planar arms* experiments

Optionally, you can install before proceeding [`geos`](http://trac.osgeo.org/geos/), it speeds up coverage computation.

Inside the cloned repository, run:
```
./install_planar_arms.sh
```

Once this is done, you can start jupyter and run the notebooks:
```
jupyter-notebook planar_arms/
```

### Installing the code for the *objects* experiments

Those experiments require many different dependencies to be installed. You will need to install [V-REP](http://www.coppeliarobotics.com/downloads.html) (version 3.2.3 was used, make sure you install the python bindings), [eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page), [FLANN](http://www.cs.ubc.ca/research/flann/), [FCL](https://github.com/flexible-collision-library/fcl) and [dmpbbo](https://github.com/stulp/dmpbbo). Some of these dependencies may be non-trivial to install; do not hesitate to contact me if you are encountering difficulties (at fabien.benureau@gmail.com), I have extensive experience on installing those on Linux and OS X systems alike.

If you are on OS X and have homebrew installed, you can run `brew install eigen flann libccd` to install some of those dependencies (`libccd` is a dependency of `FCL`).

Once all this is done, do:
```
./install_objects.sh
```

If everything went well, you can begin to interact with the notebooks:
```
jupyter-notebook objects/
```


### Reproducing results

Figure 3, 4 and 7 can be reproduced in a few seconds to a few minutes by running the Jupyter notebooks. The other figures involve extensive computation over repeated runs of the experiments. Figure 5 and 6 share the same data, which can reasonably be computed on a personal computer over a day or two at most. Figures 10 to 20 require, combined, between 1000 and 2000 hours of computation, and should probably be run on a cluster (and figures 18 and 19b need the hardware setup, unfortunately not provided when cloning this repository).

In either case, you need to go to the `figure_5/` directory of `planar_arms/`, or the `cluster/` directory of `objects/`. There, choose the figure you want to recompute data for (we choose `fig5_cluster.py` in this example), and do:

```
python fig5_cluster.py -w --hd
```

This will generate the configuration files (`--hd`), and display the jobs list (`-w`), and which are ready to be run. As reuse experiments need to exploit the data of source explorations, some jobs will need other to finish running before being ready to be executed. If all went well, do:

```
python fig5_cluster.py --run
```

Note that the program will automatically detect if the command `qstat` and `qsub` are available, and if they are, will assume it is on a cluster and try to submit jobs to it. You may want to edit the `run.pbs` (Portable Batch System) files available inside the `figure_5/`, and `cluster/` directories to match your configuration. If you edit any files, you should run `python fig5_cluster.py --hd` again. If `qstat` is not available, python will launch the jobs serially on the current machine

You will need to run `python fig5_cluster.py --run` multiple times, as new jobs become ready to execute when other finish and make their data available. If job crash for any reason, they are able to resume from the last checkpoint they made (by default, jobs save their state every 300s). You can check the number of jobs that have finished, are running, ready and waiting by running `python fig5_cluster.py -w -q`.

Please note that the job embed provenance data in their data files, gathered from the current state of the code at execution. If you don't want the provenance data to flag some of the code as dirty, you should always commit all the code (including submodule) before running jobs. Jobs check the continuity of the provenance data when resuming from a checkpoint. If it has changed, the job will restart from scratch.

Do contact me at fabien.benureau@gmail.com if any difficulties arise while trying to run experiments.
