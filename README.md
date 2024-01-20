# XVG Plotter

## Introduction

XVG Plotter is a plotting tool for xvg files based on streamlit library.

## Installation

### Anaconda

1. Run create environment command.

```shell
conda env create -f environment.yml # for windows

conda env create -f environment-linux.yml # for linux

conda activate xvg-plotter
```

2. Start streamlit app

```shell
streamlit run main.py
```

The app will be start on port 8501 and you can access by http://localhost:8501.

If you want to run on another port run:

```shell
streamlit run main.py --server.port=7500
```

### Docker

1. Pull latest firesimulations/xvg-plotter image

```shell
docker pull firesimulations/xvg-plotter:latest
```

2. Run docker container

```shell
docker run -p 7500:7500 -d --name xvg-plotter firesimulations/xvg-plotter:latest 
```

The app will be start on port 7500 and you can access by http://localhost:7500.

If you want to run on another port run:

```shell
docker run -p 8500:7500 -d --name xvg-plotter firesimulations/xvg-plotter:latest 
```

## Usage

You can plot XVG file singly or select folder for ease selection.

### Single File Analysis

![Single File Analysis - Full View](images%2F01.png)

#### Options

1. File Name: File name for saving
2. X Label: X axis label. You can give equation by adding $. for example: `Density ($m^3$)`
3. Y Label: X axis label.
4. X Index: Index of XVG file data for plotting in X axis.
5. Y Index: Index of XVG file data for plotting in Y axis.
6. Label Size: Label font size of X and Y axes. You can select `12` to `24`.
7. Plot XVG: Button for plotting.
8. Download Plot: Button for downloading image.

### Folder Analysis

![Folder Analysis - Full View](images%2F02.png)

#### Options

1. Put Project Folder: After copy and pasting project folder path, click Submit button. It will show success or error message after validating the path.
2. Select XVG File: All xvg file in the project folder will be populated here.
3. Other options are same as Single File Analysis.
