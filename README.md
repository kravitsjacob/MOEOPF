# I. File list
```
.
│   .gitignore
│   config.ini: Arguments used in `optimization.py`
│   Dockerfile: Dockerfile to run `optimization.py`
│   LICENSE
│   MOEOPF_env.yml: Conda environment to run `optimization.py`
│   optimization.py: Run the main optimization
│   README.md
│
├───borg_files
│       borg.c: Borg MOEA source code available*
│       borg.h: Borg MOEA header file*
│       borg.py: Borg MOEA python wrapper*
│       mt19937ar.c: Random number generator used by the Borg MOEA*
│       mt19937ar.h Header for random number generator used by the Borg MOEA*
│
└───MOEOPF_io
    ├───input
    │       bus_limits.csv: Voltage limits on buses
    │       costs.csv: Cost coefficients for generators
    │       emissions.csv: Emsission coefficients for generators
    │       generator_limits.csv: Generator capacity limits
    │
    └───output
            runtime.txt: Precomputed runtime files from `optimization.py`

*The Borg MOEA is freely available to academic and non-commercial users at http://borgmoea.org/. Places these files EXACTLY as they appear in the above tree.
```

# II. How to Run
This tutorial assumes the use of gitbash or a Unix-like terminal with github command line usage
1. Clone the repository using `$git clone https://github.com/kravitsjacob/MOEOPF.git`
2. Download and Run Docker Desktop. For more information on Docker visit: https://docs.docker.com/desktop/. To ensure 
that it is installed correctly go to the command prompt/terminal and enter `$docker --version`
3. Get a [Borg MOEA license](http://borgmoea.org/) and place the required files in the `borg_files` folder. Your tree should look EXACTLY as the one above.
3. Change to the current working directory using command prompt/terminal `$cd <insert_path_to_/MOEOPF>`
4. Build the docker image by running `$docker build --tag optimization .`
5. Run the image and mount output data by running `$docker run -v /$(pwd)/MOEOPF_io/output:/MOEOPF/MOEOPF_io/output optimization`
     * This process will take a long time as this is the serial verison of the optimization.
     * Pre-computed outputs have been supplied in `/MOEOPF_io/ouput`

# III. Citing this work
Look [here](https://osf.io/fd3mj/) for more information about this work. Please use the following citation
```
@article{kravits_multi_2021,
         title = {Multi-Objective Optimal Power Flow Considering Emissions and Voltage Violations},
         url = {http://kyrib.com/Papers/Kravits_PES_GM_2021.pdf},
         journal = {Proceedings of the 2021 Power and Energy Systems General Meeting},
         author = {Kravits, Jacob and Baker, Kyri and Kasprzyk, Joseph},
         year = {2021},
}
```


