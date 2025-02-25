# Conda Commands

## Create Conda Environment
    conda env create -f environment.yml

## Activate Environment
    conda activate base

## Update Dependencies
    conda env export > environment.yml
    conda env update --file environment.yml --prune

## Deactivate Environment
    conda deactivate


# Naming Conventions for Notebooks
Adapted from [cookie cutter datascience guidelines](https://cookiecutter-data-science.drivendata.org/using-the-template/)

Example Name: **0.01-pjb-data-source-1.ipynb**

Name of notebooks have 3 parts:


### 0.01 - Phase.Notebook
- 'Phase':  The phase of the analysis
- 'NOTEBOOK': The Nth notebook in that phase to be created.

#### **Project Phases**
0. **Data Exploration**
1. **Haunted Feature Creation**
    Features from Assignment:
    - Audio Evidence | *1.01-dg*
    - Visual/Video Evidence | *1.02-dg*
    - Haunted Places Date | *1.03-dg*
    - Haunted Places Witness Count | *1.04-dg*
    - Aparition Type | *notebook*
    - Event Type | *notebook*
    - Time of Day | *notebook*
2. **Joining Datasets**
    - [Alcohol_Dataset](https://drugabusestatistics.org/alcohol-abuse-statistics/)
    - [Daylight_Dataset_Timeanddate](https://www.timeanddate.com/astronomy/usa) 
    - [Daylight_Dataset_Navy](https://aa.usno.navy.mil/data/Dur_OneYear)
    - [flights_dataset](https://openflights.org/data.php#route)
        - [airports](https://ourairports.com/data/)
    - [Custom_Dataset_2]
    - [Custom_Dataset_3]
3. **Visualizations**
4. **Modeling/Inference**
5. **Publication**

### **pjb** (Initials of Coder)
Ensures authors get credit. Prevents collisions in coding as well.

### **data-description**
All descriptions written in snake_case
- 'data': Dataset Used
- 'description': Purpose of Notebook
