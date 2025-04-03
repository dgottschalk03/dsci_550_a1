# Named Entity Recognition Report

This report is comprised of all findings from the [SpaCY_analysis_notebook](../notebooks/1.09-dg-hpv2-named_entities.ipynb). 

## **Named_Entities**


### **Format**
  - list [(entity, label), ...]
  - Default Value : []

  - Named Entities : 
      - CARDINAL
      - DATE
      - EVENT
      - FAC
      - GPE
      - LANGUAGE
      - LAW
      - LOC
      - MONEY
      - NORP
      - ORDINAL
      - ORG
      - PERCENT
      - PERSON
      - PRODUCT
      - QUANTITY
      - TIME
      - WORK_OF_ART
 
### **Method**

Used [SpaCYs en_core_web_trf](https://spacy.io/models/en#en_core_web_trf).
  - trained on written blogs, news, and comments
  - Highest F1 score of pre-trained models (0.90)
  - Disabled unnecessary modules to speed up computation
      - parser
      - attribute_ruler
      - lemmatizer

---


### **For Graders**

  - I consolodated all of the markdown cells into a [report]("../reports/namedEntityRecognitionReport.md). :point_left: 

There are 4 major sections:
  - **Feature Extraction** 
    - extract named entities
    - count occurence of each named entity using `collections.Counter`
  - **SpaCY Performance** 
    - Coverage Analysis
    - entity label distribution
    - Highlight cool entities  
  - **Improving on Assignment 1** 
    - Improve [extract_dates](./dsci_550_a1/parsingFunctions.py) and [classify_time_of_day_v2](./dsci_550_a2/parsingFunctions_v2.py) from A1 using named entities as edge cases.
    - Document changes made to functions and coverage improvements. 
  - **Regenerated A1 Features**
    - rerun A1 scripts with new and improved functions. Table of improved performance below :point_down:

|    |   Time_of_Day |   Haunted_Places_Date |
|:---|--------------:|----------------------:|
| v1 |       32.84\% |               25.48\% |
| v2 |       **35.34**\% |               **27.57**\% |


**Final Note**:
  - I looked into using tools like [label_sudio](https://labelstud.io/) to curate a training set and fine tune our model to haunted places. However, in order to parse for custom entities like ("GHOST", "DEMON", etc.), we would need an annotated dataset of 1,000s of entities of each type. **We would have to train on almost the entire haunted places dataset**. 

---
---

## **SpaCY Performance**

What can SpaCY tell us about our haunted places?

---

#### Coverage
  - SpaCY extracted **34044** total entities.
  - **83.52%** of our haunted places had at least 1 named entity. 
  - **Date**, **Time**, and **FAC** had the highest coverage

 |          |   %_Coverage |   Extracted_Entities |
|:---------|-------------:|---------------------:|
| Total    |        83.52 |                34044 |
| DATE     |        39.52 |                 7168 |
| TIME     |        33.25 |                 4927 |
| FAC      |        26.72 |                 4474 |
| CARDINAL |        25.15 |                 4340 |
| PERSON   |        17.84 |                 3486 |
| ORG      |        15.16 |                 2341 |
| GPE      |        13.02 |                 2132 |

---

#### Uniqueness
  - SpaCy extracted **14921** unique entities total. Ratio of unique to total is **43.83\%** 

  - **Most unique entity types** - **FAC**, **DATE**, and **PERSON**. 
    - Makes intuitive sense, most people, places, and dates are unique.
  - **Dates are often repeated** - only have a uniquness ratio of **33.27%** despite their high coverage across our dataset.

 |        |   Unique_Entities |   Extracted_Entities |   %_Unique_Ratio |
|:-------|------------------:|---------------------:|-----------------:|
| Total  |             14921 |                34044 |            43.83 |
| FAC    |              3836 |                 4474 |            85.74 |
| DATE   |              2385 |                 7168 |            33.27 |
| PERSON |              2170 |                 3486 |            62.25 |
| ORG    |              1893 |                 2341 |            80.86 |
| GPE    |              1344 |                 2132 |            63.04 |
| TIME   |               833 |                 4927 |            16.91 |
| LOC    |               815 |                  935 |            87.17 |

---

#### Top Entities

 |    | PERSON            | PRODUCT                     | ORG                             | FAC                   | GPE                  | LOC                            | NORP                     | DATE                     | TIME                     |
|---:|:------------------|:----------------------------|:--------------------------------|:----------------------|:---------------------|:-------------------------------|:-------------------------|:-------------------------|:-------------------------|
|  0 | ('Mary', 64)      | ('Calvary', 4)              | ('Inn', 57)                     | ('Auditorium', 23)    | ('Chicago', 21)      | ('Gravity Hill', 7)            | ('Indian', 249)          | ('this day', 169)        | ('night', 1715)          |
|  1 | ('George', 49)    | ('911', 3)                  | ('Union', 30)                   | ('Cemetery', 15)      | ('Ohio', 20)         | ('Bandera Pass', 6)            | ('Indians', 122)         | ('today', 115)           | ('late at night', 499)   |
|  2 | ('Alice', 30)     | ('Zodiac', 3)               | ('KKK', 19)                     | ('Main Street', 14)   | ('California', 16)   | ('the Ohio River', 4)          | **('Confederate', 50)**      | ('years', 113)           | ('midnight', 208)        |
|  3 | ('Elizabeth', 28) | **('EverQuest', 2)**            | **('NASA', 16)**                    | ('Mansion', 12)       | ('Indiana', 15)      | ('Mississippi', 4)             | ('Native American', 44)  | ('the years', 110)       | ('the night', 198)       |
|  4 | ('John', 24)      | ('the Steel Phantom', 2)    | ('University', 13)              | ('Chapel', 11)        | ('Texas', 13)        | ('Slippery Rock Creek', 3)     | ('British', 28)          | ('the day', 102)         | ('one night', 155)       |
|  5 | ('Joe', 20)       | ('Colossus', 2)             | ('Wal-Mart', 11)                | ('Fort', 8)           | ('England', 12)      | ('an Indian Burial Ground', 3) | ('Spanish', 23)          | ("the early 1900's", 96) | ('nights', 114)          |
|  6 | ('Sarah', 18)     | ('The Goat Man', 2)         | **('YMCA', 11)**                    | ('Crybaby Bridge', 7) | ('Michigan', 11)     | ('Hills', 3)                   | ('Catholic', 20)         | ('years ago', 87)        | ('hours', 109)           |
|  7 | ('Charlie', 16)   | ('Impala', 2)               | ('Paramount', 11)               | ('Smith Hall', 7)     | ('US', 11)           | ('Beaver Creek', 3)            | **('confederate', 20)**      | ('many years ago', 86)   | ('Late at night', 96)    |
|  8 | ('Molly', 14)     | ('Roadrunner', 2)           | ('Hotel', 9)                    | ('Alumni Hall', 7)    | ('Pennsylvania', 10) | ('Lake Ontario', 3)            | ('Native Americans', 16) | ('many years', 85)       | ('One night', 71)        |
|  9 | ('Hannah', 14)    | ('HELP', 2)                 | ('Church', 9)                   | ("St. Mary's", 7)     | ('Illinois', 10)     | ('Island', 3)                  | ('Chinese', 16)          | ("the 1800's", 83)       | ('every night', 65)      |
| 10 | ('David', 12)     | ('H-1', 2)                  | ('the Underground Railroad', 7) | ('High School', 7)    | ('America', 9)       | ('South', 3)                   | ('French', 14)           | ('Halloween', 82)        | ('the morning', 58)      |
| 11 | **('Jesus', 12)**     | ('The Green Lady', 2)       | ('Academy', 6)                  | ('Main St.', 6)       | ('NY', 9)            | ('gravity hill', 3)            | ('German', 14)           | **('June 2008', 76)**        | ('morning', 34)          |
| 12 | ('Tommy', 12)     | ('the Greenbriar Light', 2) | ('Haunted Places', 6)           | ('Wilson Hall', 6)    | ('Missouri', 9)      | ('choate', 3)                  | ('Irish', 13)            | ("the late 1800's", 69)  | ('the next morning', 32) |
| 13 | ('Annie', 12)     | ('Torries', 2)              | ('State', 6)                    | ('Broadway', 6)       | ('Georgia', 9)       | ('Earth', 3)                   | ('Hawaiian', 13)         | **('March 2008', 58)**       | ('that night', 30)       |
| 14 | **('Al Capone', 11)**| ('Cheyenne', 2)             | ('Wal', 6)                      | ('Bridge', 6)         | ('Tennessee', 9)     | ('Lake', 3)                    | ('English', 12)          | ('the 1800', 54)         | ('dusk', 23)             |

---

#### :mag: Fun Observations
  - **Jesus** - **"Jesus"** is the 12th most common *PERSON* entity with 12 counts. 
    - **"Al Capone"** is close behind with 11 counts.
    - **"Satan"** only has 4 mentions
  - **EverQuest** - Guess we best stick to Runescape. 
  -  **YMCA** - It is not fun to stay in here. 
    - "Nasa" is also quite haunted. **No mentions of JPL in our dataset though.**
  - **Civil War** - Many mentions of "confederate". **Looks like they lost the war.**  
    - Only 30 mentions of "Union". 
  -  **Financial Crisis** - Most common dates are "June 2008" and "March 2008". 
    - **Stocks weren't the only thing scaring people in 2008**
  - **WORKS_OF_ARE** - "Bible" most common work of are with 11 mentions.
    - "West Side Story" comes in second with 3. 

---

#### 📝 Conclusion and Connection to A1

In Conclusion SpaCy entities tell us a lot about our dataset. 

- **Storytelling** - More in depth labels like **PERSON** and **ORG** tell us what the important figures are across our dataset.

- **Improved Parsing** - SpaCY entities revealed edge cases to our previous methods in A1. I document the changes in the [codebook](../notebooks/1.09-dg-hpv2-named_entities.ipynb).

- **Visualize our Data** - Histograms below are a cool way to visualize what author's believe are the most relevant entities for a haunted place. 
  - **DATE** , **TIME**, **FAC** are the most relevant to a haunted place. 

- **Keyboard Warrior** :musical_keyboard: - Common dates like **March 2008** and **June 2008** revealed a spur of updates made to the dataset. **Updates appear to be from a single,opinionated writer.**
  - The majority of updates are **corrections** removing haunted places or **discouraging** people from entering:
    - 2343 ~ _"June 2008 Removed. No Murder has happened here."_
    - 1589 ~ _"May 2008 Update – The Statue of Jesus to even exist is questionable._"
    - 1424 ~ _"...March 2008 Update – up until the 1870s muskets did not use brass shells, but paper cartridges with black powder or just black powder with a ball. So brass shells would have nothing to do with the Revolutionary War."_

---

## 🛠 Improving upon  Assignment 1

SpaCY entities revealed critical oversights we made from Assignment 1. 

I improved the following from assignment 1:
- **DATE** - **`extract_dates`**
- **TIME** - **`classify_time_of_day`**

**Feature coverage after changes:**
|    |   Time_of_Day |   Haunted_Places_Date |
|:---|--------------:|----------------------:|
| v1 |       32.84\% |               25.48\% |
| v2 |       **35.34**\% |               **27.57**\% |

See sections below for more details. 

---

### **DATE**

How do the **"DATE"** entities improve upon our existing **"Haunted_Places_Date"** feature? 

---

#### 🧭 Adding Context to Haunted Places
- SpaCy recognizes the following:
  - **Seasons** — e.g., `("Winter", 13)`, `("Summer", 55)`
  - **Holidays** — e.g., `("Halloween", 82)`, `("Christmas", 14)`
  - **Individual Months** — e.g., `("December", 13)`, `("October", 18)`
  - **Relative Dates** — e.g., `("this day", 169)`, `("Many years ago", 33)`

---

#### 🔧 Improving `extract_dates` from Assignment 1

- **extract_dates from assignment 1** only captured **45%** of the top 100 most common "DATE" entities. Of these entities, we missed:

```
    | Missed Entity       | Enhancement|                                                                 
    |:---------------------|------------------------------------------------------------------------------:|
    | **"1800s"**          | Updated regex to allow optional "s": `(?:\s*'?s)?`                          
    | **Double Years**     | Modified `clean_dates` to remove duplicate years                            
    | **"20th Century"**   | Added regex: `\b\d{1,2}(?:st|nd|rd|th)?\s*century\b`                        
    | **Holidays**         | Introduced regex patterns using `Holiday_patterns` dictionary at function top 
    |                     | Holidays stored as `[1000, [month], [day]]`                                 
```


---

All of these improvements were compiled into the new **`extract_dates`** function, located [here](../dsci_550_a1/parsingFunctions.py)

```
./dsci_550_a1/parsingFunctions.py
```

#### 📝 Conclusion

| Method              | Coverage of top 100 entities | Total Coverage |
|:---------------------|------------------------------|----------------:|
| **extract_dates**   | 43%                          | 23%            |
| **extract_dates_v2**| **67%**                      | **41.17%**     |


In Conclusion SpaCy the "DATE" entities:
- **revealed edge cases**: 
    - After improvements, `extract_dates` captures **67%** of the top 100 most common "DATE" entities
    - Overall, `extract_dates` now covers **41.17%** of all "DATE" entities
- **contextualize the timeline of a haunted place**: 
    - Entities like "the next day" provide context for the duration of a haunted event.
      - Did it occur over one day? over multiple? overnight? ..etc. 

---

### **TIME**

**How does _"TIME"_ improve upon _Time_of_Day_?**

---

#### 🏚️ Added Context to Haunted Place

- Named entities provide context for the **duration of events** that _Time_of_Day_ does not:
  - **"a few minutes later"**
  - **"the next day"**
  - **"seconds before"**
- These features don't fit into the limited categories of _Time_of_Day_, but help provide **temporal context** to narratives.

---

#### 🛠 Improving upon `classify_time_of_day` from Assignment 1

- **`classify_time_of_day` from Assignment 1:**
  - Captured **57%** of the top 100 most common "DATE" entities
  - Captured only **36.37%** of all "DATE" entities overall

- Here are some missed entities and how we addressed them:

```

| Missed Entities                            | Fix / Enhancement                                                                 |
|--------------------------------------------|------------------------------------------------------------------------------------|
| **"nights", "evenings", "mornings"**       | Added suffix regex: `('s|s)?`                                                     |
| **"overnight", "morningtime"**             | Used more general regular expressions with lemmatization                          |
| **"Afternoon", "All Hours", "all day"**    | Added new feature values: **"Afternoon"**, **"All Day"**                          |
| **"3 pm"**                                  | Created `classify_hours` function to parse specific times of day                  |
| **"school hours", "closing hours"**        | Used regex: `\b(?:school|business|work|day|lunch|dinner|daytime)\s*hours?\b`      |

```
---

All of these improvements were compiled into the new **`classify_time_of_day_v2`** function, located [here](../dsci_550_a2/parsingFunctions_v2.py)
```
./dsci_550_a2/parsingFunctions_v2.py
```