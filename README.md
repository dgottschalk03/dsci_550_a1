# DSCI_550_A1

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Analysis of the Haunted Places Dataset. Assignment 1 for DSCI_550 SP 25. 

Due | 3-14-2025

    



## Project Organization

```
├── README.md          <- The top-level README.
|
├── clones             <- Store cloned ettlib and tika-similarity repos 
│
├── clustering         <- Clustring output 
│
├── data
│   ├── joined_datasets<- Datasets joined to haunted_features
│   ├── keywords       <- Keywords used in feature extraction. Used in notebooks [1.01, 1.02, 1.04, 1.05, 1.08]
│   ├── processed      <- The final, canonical data sets for modeling. Also includes intermediary da
│   |   |
|   │   ├── *features_added.tab | final dataset 
|   │   ├── *cleaned.tab        | og dataset with stopwords removed and NAN values filled
|   |   ├── *flight*.json       | jsons used for html visualization in notebooks [3.01-3.03]
│   |── raw            <- The original haunted places dataset
│   └── Tika-Similarity<- Stores outputs for tsv2json and conf files used in clustering.
│
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, dataset used, and a short `_` delimited description.
|                         Fields delimited by '-'. e.g.
│                         `1.0-jqp-dataset_1-data_exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         dsci_550_a1 and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── environment.yml    <- Conda environment used to run notebooks 
|
├──  python_3_10.yml    <- Conda environment to run tika-similarity and ettlib (python > 3.10 not supported)
│                         
│
└── dsci_550_a1   <- Source code for use in this project.
    │
    ├── __init__.py                    <- Makes dsci_550_a1 a Python module
    │
    ├── clusterHelper.py               <- Helper function to compute similarity .csvs
    │
    ├── clusterWorkflow.py             <- Script to run full cluster workflow using tika-similarity and ettlib
    │
    ├── flightFunctions.py             <- Flight functions [notebooks 2.01, 3.01-3.03]
    |
    ├── haunteddateday.py              <- Script used to generate haunted_place_time_of_day
    |
    ├── add_daylight_data_columns.py   <- Script used to join Daylight_Duration_Hours
    |
    │
    ├── csv2tab                        <-  Used to convert initial dataset from .csv to .tab
    |
    ├── parsingFunctions.py            <- Functions used for parsing [notebooks 1.01-1.05]
    |
    |    - extractSequences   | sequences tokens by sentences 
    |    - check_regex        | check precompiled regex pattern
    |    - extract_dates      | calculated "Haunted_Places_Date" 
    |    - clean_dates        | Remove invalid dates
    |
    ├── unpack_circles.py              <- Unpacks */circles.json and */cluster.json from clusterWorkflow.py
    |
    |   - unpack_cluster     | returns cluster names and haunted places indicies in said cluster.
│
│
│
```

--------

## Group Members
* Daniel Gottschalk
* Reha Matai
* Serafina Smith
* Mikena Moore
* Kate Mathew



## Naming Conventions for Notebooks
Adapted from [cookie cutter datascience guidelines](https://cookiecutter-data-science.drivendata.org/using-the-template/)

Example Name: **01.01-dg-haunted_places-audio-evidence.ipynb**
- **phase** | 1.01
- **initials** | dg
- **data** | haunted_places
- **description** | audio_evidence
Name of notebooks have 3 parts:


### 0.01 - Phase.Notebook
- 'Phase':  The phase of the analysis
- 'NOTEBOOK': The Nth notebook in that phase to be created.

### **pjb** (Initials of Coder)
Ensures authors get credit. Prevents collisions in coding as well.

### **data-description**
All descriptions written in snake_case
- 'data': Dataset Used
- 'description': Purpose of Notebook



## **Project Overview**

Click on contributor's initials to see file. 

0. **Data Exploration**
- fillNAN and Cleaining | [dg](notebooks/0.01-dg-raw_data-fillna_init_output.ipynb)
- Stopword Cleaning | [dg](notebooks/0.02-dg-raw_data-data_cleaning.ipynb)


1. **Haunted Feature Creation**
Features from Assignment:

- Audio Evidence | [dg](notebooks/1.01-dg-haunted_places-audio_features.ipynb)
- Visual/Video Evidence | [dg](notebooks/1.02-dg-haunted_places-visual_features.ipynb)
- Haunted Places Date | [dg](notebooks/1.03-dg-haunted_places-date_features.ipynb)
- Haunted Places Witness Count | [dg](notebooks/1.04-dg-haunted_places-witness_features.ipynb)
- Event Type | [rm_dg](notebooks/1.05-dg_rh-haunted_places-events_type.ipynb)
- Aparition Type | [rm](notebooks/1.06-rm-haunted_places-apparition_type.ipynb)
- Time of Day | [rm](notebooks/1.07-rm-haunted_places-time_of_day.ipynb) 


2. **Joining Datasets**
- [OpenFlights](https://openflights.org/data.php#route) and [OurAirports](https://ourairports.com/data/) | [dg](notebooks/2.01-dg-airports_data-joining.ipynb)
    - **MIME TYPE** | *Multi-Part/\**
    - **Features** | *{Aerodrome_Count, Aerodrome_Proximity, Flight_Intersection_Count, Flight_HighTraffic}*
- [Place_Of_Worship](https://hub.arcgis.com/datasets/openstreetmap::openstreetmap-places-of-worship-for-north-america/about) | [ss](/notebooks/2.02-ss-Places_of_Worship-joining.ipynb)
    - **MIME TYPE** | *Application/\**
    - **Features** | *{Distance_to_Nearest_Worship, Haunted_Place_Proximity, Religion_Intersection}*
- [BRFFS_Mental_Health]() | [ss](notebooks/2.03-ss-mental_health_data-joining.ipynb)
    - **MIME TYPE** | *Text/\**
    - **Features** | *{Average_Mental_Health_Days, Average_Poor_Health_Days, Depression_Prevalence}*
- [Alcohol_Dataset](https://drugabusestatistics.org/alcohol-abuse-statistics/) | [rm](notebooks/2.02-rm-alcohol_abuse-join.ipynb)
- [Daylight_Hours_Dataset](https://sunrise-sunset.org/api) | [km](./dsci_550_a1/haunteddateday.py)

3. **Visualizations**
- [Airborne_Events.html](notebooks/3.01-dg-haunted_places-airborne_events_plot.ipynb) | [dg]
    - Plot generated using plotly.go
    - Plots 199 haunted places with their intersecting routes and airports
    - All haunted places flagged with either *{Plane_Crash, Electronic_Malfunction, Flying_Object}*
    - Uncomment last line to write html file
- [mostHauntedAirports.html](notebooks/3.02-dg-HP_Features_Added-haunted_airports_plot.ipynb) | [dg]
    - Plots 10 most haunted airplane routes
    - Plots 10 most haunted airports of each type
    - Plots every haunted event color coded by apparition type


4. **Clustering/Inference**
- Clustering Flight Features | [dg](notebooks/4.01-dg-HP_Features_Added-Flight_Clusters.ipynb)
- Clustering Religion Features | [sm_rm](notebooks/4.02-ss_rm-haunted_places_features-religion_cluster.ipynb)
- Clustering Mental Health Features | [sm_rm](notebooks/4.03-ss_rm-haunted_places_features-mental_health_cluster.ipynb)
- Clustering Alcohol Features | [sm_rm](notebooks/4.04-ss_rm-haunted_places_features-alcohol_cluster.ipynb)
- Clustering using [Apparition_Type, Event_Type, and Time_of_Day] as features |  [mm](clustering/mikenaClustering)
- 

5. **Report Writeup**
**dg**
- wrote **Open Flights Results** and **Open Flights** portions of report

**km**

**mm**
- Wrote portion of the report about the Apparatition features
- Wrote portion of the report about correlations between keywords and Apparition types 
- Wrote portion of the report about the co-occurring features and locations
- Wrote portion of report introducing and describing the datasets

**rm**
- Wrote portion of report about the Alcohol Abuse related clusters and discussed which locations more likely to be influenced by alcohol abuse that cause more Haunted Places to be reported
- Wrote portion of report about pros/cons of Apache Tika

**ss**
- Wrote portion of report about how the Mental Health related features were extracted and about the clusters.
- Wrote portion of report about how the Places of Worship related features were extracted and about the clusters.

6. **Other Contributions**

**dg**
- Project manager
    - wrote README.md
    - organized github and directories
- Wrote [cluster workflow functions](dsci_550_a1/clusterWorkflow.py) [helper functions](dsci_550_a1/clusterHelper.py) used by group to perform clustering

**km**

**mk**

**rm**

**ss**