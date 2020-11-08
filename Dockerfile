FROM continuumio/miniconda3
RUN conda install -c invenia pandapower
WORKDIR /app
ADD borg_files /app
COPY ["optimization.py", "/app/"]
ENTRYPOINT ["python", "-u", "optimization.py"]

