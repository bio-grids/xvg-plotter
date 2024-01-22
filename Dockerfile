FROM continuumio/miniconda3:23.10.0-1

LABEL authors="Dilwar Hossain Noor"

WORKDIR /app

COPY environment-linux.yml .

RUN conda env create -f environment-linux.yml

#SHELL ["conda", "run", "-n", "xvg-plotter", "/bin/bash", "-c"]

COPY . .

EXPOSE 7500

ENV IS_DOCKER 1

ENV PATH /opt/conda/envs/xvg-plotter/bin:$PATH

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=7500", "--server.address=0.0.0.0"]
