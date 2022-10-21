# Replication Package of Task-Oriented ML/DL Library Recommendation based on Knowledge Graph
## Empirical Study
- [1000 ML/DL Related Posts.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/empirical_study/empirical_data_sample.xlsx)
This csv file contains 1000 questions randomly selected from the Stack Overflow data dump meeting all 
the criteria in the paper. In the csv file, the column “Title” represents the title of corresponding 
post, “Url” represents Stack Overflow url for posts, “Annotator_1” represents the annotation of the 
first annotator, “Annotator_2” represents the annotator of the second annotator.

- [Task and Factor Analysis of 283 Posts.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/empirical_study/empirical_data_annotation.xlsx)
This file contains 283 posts from 1000 posts which both annotators labeled true for seeking ML/DL 
libraries. In the csv file, “Title” represents the title of corresponding post, “Url” represents 
Stack Overflow url for posts, “Accepted answer” represents whether the post has accepted answer or not.
Besides, “Task” represents the task included in the post, “Task category” is the corresponding 
category of the task, “Resource type” describes whether askers first want is model or implementation, 
“Factor” represents 11 main factors contained in the post. All these four columns are arbitration of 
two annotators.

## Task Categories
- [Task Categories of PapersWithCode.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/task_categories.json)
This json file contains the task categories we collected from PapersWithCode. 

## Pattern Description
- [Complete List and Descriptions of the Patterns.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/pattern_description.xlsx)
We summarize a set of patterns for the extraction of some implementation knowledge from ReadMe files.
These patterns involve not only linguistic patterns in the text but also the section structure, hyperlinks, and code blocks of the ReadMe file. 

## KG Construction
[The Module of Knowledge Graph Construction.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/kg_construction/)
This module is used to construct knowledge graph, including the definition of entity relation, generation of entity relation and construction of knowledge graph.
- [The Definition of Entity Relation.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/kg_construction/entity_relation_category.py)
This code file defines all the entity categories and relation categories in the knowledge graph. This is the first step in building the knowledge graph.

- [The Generation of Entity Relation.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/kg_construction/entity_relation_generator.py)
Based on the definition of entity relation, this code file implements the generation of all pre-defined entity and relation triples. We have implemented different functions to generate entity information for different entities.

- [The Construction of Knowledge Graph.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/kg_construction/kg_constructor.py)
Based on the entity and relation data generated in the previous step, this code file implements the construction of the knowledge graph. It mainly includes the import of various entities and relation building, and finally generates the AI task-model knowledge graph.

## Resulting KG
The resulting AI task-model KG includes 159,310 entities and 628,045
relationships. The entities include 17,250 tasks, 25,404 papers, 25,718
models, 21,003 model implementations, and 24,047 repositories. The relationships 
include 17,410 subclassOf relationships between tasks, 44,438 accomplish 
relationships, 20,594 hasEvaluation relationships, 29,281 implement relationships, 
21,008 provide relationships, 60,040 basedOn relationships, and 105,963
support relationships.

The complete data of the resulted KG will be disclosed in case of accepted. 

## Recommendation
[The Recommendation of ML/DL Library.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/lib_recommendation/)
This module implements the ML/DL library recommendation. 
It provides recommendations for libraries, filtering and sorting of results, keyword hints and calculating scores of various indicators.

## Experiments
- [RQ1: Intrinsic Quality of Knowledge Graph.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ1/)
    - [384 Tuples in the KG.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ1/KG_tuples_for_intrinsic_quality_evaluation.xlsx)
We randomly sample 384 tuples from the KG and ensure that each type of relationships and attributes has at least 20 tuples selected. 
The "Start entity" represents the start node of the relation, "End entity" represents the end node of the relation, 
"Auxiliary" is used to help annotators label easier, “Annotator_1” represents the annotation of the first annotator, “Annotator_2” 
represents the annotator of the second annotator, "Arbitration" represents the arbitration between two annotators. 
    - [Accuracy per Tuple Type.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ1/Accuracy_per_tuple_type.xlsx)
The statistic results of accuracy per tuple type is shown here.

- [RQ2: Trends of AI Tasks and Implementations Analysis.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ2/)
MLTaskKG links AI tasks, ML/DL models, and their implementations in a knowledge 
graph, thus we analyze the trends of AI tasks and their implementations. The 
analysis can help application developers to have an overview of the implementing
repositories for different AI tasks and the emergence of new ML/DL models and
implementations for specific AI tasks.

- [RQ3: AI Task-Model KG Effectiveness Evaluation.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3/)
We evaluate the effectiveness of MLTaskKG by conducting a human
study. In the study we ask a set of participants to use MLTaskKG to
find suitable ML/DL libraries for given AI tasks and use 
PapersWithCode as a baseline for comparison. 
    - [ML/DL Library Retrieval Tasks.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3/Tasks.docx)
We randomly select eight questions aimed at seeking for ML/DL libraries from our
empirical study data and adapt them into eight ML/DL library retrieval tasks.
    - [Experiment Design.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3/)
We invite 10 MS students to participate and divide
them into two “equivalent” participant groups (PA and PB).
On the other hand, we randomly divide the eight
tasks into two task groups (TA and TB) as well. For each task the 
participants need to record a most suitable ML/DL library 
(i.e., GitHub repository) that meets the requirements of the task 
as the result and completion time for each task. After that, We invite 
another 4 MS students to assess the satisfaction of each submitted result 
on a 4-points Likert scale (1- disagree; 2-somewhat disagree; 
3-somewhat agree; 4-agree). Finally, we measured satisfaction and 
completion time and drew a box plot. 
    - [Results of Satisfaction Statistics.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3/Satisfaction_Number_Statistics.xlsx)
We summarize satisfaction of each submitted result using MLTaskKG and PapersWithCode.

It is hereby stated that due to anonymity, some information is hidden and will be disclosed in the future.
