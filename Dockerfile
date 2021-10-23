FROM continuumio/miniconda3
WORKDIR /MOEOPF

# Create the environment:
COPY MOEOPF_env.yml .
RUN conda env create -f MOEOPF_env.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "MOEOPF_env", "/bin/bash", "-c"]

# Create borg shared object
ADD borg_files /MOEOPF
RUN gcc -shared -fPIC -O3 -o libborg.so borg.c mt19937ar.c -lm

# Run optimization
ADD MOEOPF_io /MOEOPF/MOEOPF_io
COPY optimization.py .
ENTRYPOINT ["conda", "run", "-n", "MOEOPF_env", "python3", "-u", "optimization.py"]
