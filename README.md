# jupyter-microscopy

Collection of tools for working with microscopy data in jupyter notebooks.

Outside of this repo some useful tools are:  
  
manual image segmentation: [ipysegment](https://github.com/ianhi/ipysegment)   
colony counting: [skimage counter](https://github.com/jrussell25/colony_counter)  
colony counting2: [web tool](https://github.com/ianhi/colony-counter)  
choose points of interest and output files of the points: [laser pointer](https://github.com/Hekstra-Lab/laser-pointer)


## Why?

I prefer python over ImageJ for analyzing microscopy images, but I really miss the nice interactive image viewing provided imagej. The point of this repo is keep all the microscopy image tools I might make in a single place. I'll strive to replicate the most useful manual interaction tools provided by ImageJ in such a way to be useful to an advanced python user. Three key goals:
1. Limit distance to data
   - Should always be trivial to extract the data from manual interaction to a numpy array
2. Should *feel* good to use
   - I don't want my tools to make me sad, only my experiment not working gets to do that...
3. Doesn't look gross
   - similar to the above, so many people have thought hard about web design surely I can make use of some of that. 
   
   


## Design

- Use [PIMS](https://github.com/soft-matter/pims) to store image data
   - no reason to reinvent the wheel on this on
- components hopefully slot in well together



## Setting up a conda environment

I used the following bash commands to create envs. Add them to your `.bashrc`, do `source ~/.bashrc` and then run `jlab-env-full micro`

```bash
jlab-env-basic ()
{
    conda create -n $1 --override-channels --strict-channel-priority -c conda-forge -c anaconda jupyterlab nodejs python mamba -y
     conda activate $1
}

jlab-env-full ()
{  
  conda create -n $1 python -y
  conda activate $1
  conda install -c conda-forge mamba -y
  mamba install -c conda-forge jupyterlab nodejs scipy matplotlib numpy ipympl pandas -y
  pip install jupyterlab-git
  jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
  jupyter lab build --name=$1
}

```