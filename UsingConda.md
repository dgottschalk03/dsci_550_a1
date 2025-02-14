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
- 'Phase':  The phase of the analysis
- 'NOTEBOOK': The Nth notebook in that phase to be created.

#### **Project Phases**
1. **0 - Data Exploration**
2. **1 - Haunted Feature Creation**
    Features from Assignment:
        - Audio Evidence | Tool Used
        - Visual/Video Evidence | Tool Used
        - Haunted Places Date | Tool Used
        - Haunted Places Witness Count | Tool Used
        - Aparition Type | Tool Used
        - Event Type | Tool Used
        - Time of Day | Tool Used
3. **2 - Joining Datasets**
    - [Alcohol_Dataset](https://drugabusestatistics.org/alcohol-abuse-statistics/)
    - [Daylight_Dataset_Timeanddate](https://www.timeanddate.com/astronomy/usa) 
    - [Daylight_Dataset_Navy](https://aa.usno.navy.mil/data/Dur_OneYear)
    - [Custom_Dataset_1]
    - [Custom_Dataset_2]
    - [Custom_Dataset_3]
4. **3 - Visualizations**
5. **4- Modeling/Inference**
6. **5- Publication**

### **pjb** (Initials of Coder)
    Ensures authors get credit. Prevents collisions in coding as well.

### data-description
All descriptions written in snake_case
- 'data': Dataset Used
- 'description': Purpose of Notebook
