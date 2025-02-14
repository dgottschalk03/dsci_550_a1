# Conda Commands

## Create Conda Environment
conda env create -f environment.yml

## Activate Environment
conda activate pyenv

## Update Dependencies
conda env export > environment.yml
conda env update --file environment.yml --prune

## Deactivate Environment
cond deactivate pyenv


# Naming Conventions for Notebooks
    Adapted from [cookie cutter datascience guidelines](https://cookiecutter-data-science.drivendata.org/using-the-template/)

Name of notebooks have 3 parts:
    0.01-pjb-data-source-1.ipynb

### 0.01 - Phase.Notebook
Phase is the phase of the analysis
NOTEBOOK is just the Nth notebook in that phase to be created.

Project Phases:
    0 - Data exploration 
    1 - Haunted feature creation {Audio Evidence, Visual/Video Evidence , Haunted Places Date, Haunted Places Witness Count, Aparition Type, Event Type, Time of Day} 
    2 - Joining Datasets:
        * [Alcohol_Dataset](https://drugabusestatistics.org/alcohol-abuse-statistics/)
        * [Daylight_Dataset_Timeanddate](https://www.timeanddate.com/astronomy/usa)
        * [Daylight_Dataset_Navy](https://aa.usno.navy.mil/data/Dur_OneYear)
        * [Custom_Dataset_1]
        * [Custom_Dataset_2]
        * [Custom_Dataset_3]
    3 - Visualizations - often writes publication-ready viz to reports
    4 - Modeling/Inference - training machine learning models
    5 - Publication - Notebooks that get turned directly into reports

### pjb 
Initials of Coder; this is helpful for knowing who created the notebook and prevents collisions from people working in the same notebook.

### data-description
    data - dataset used
    description - what notebook does
