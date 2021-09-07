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

## Pattern Description
- We extract implementation knowledge from ReadMe files using some 
predefined patterns.


| <sub>Knowledge Type</sub> | <sub>Definition</sub> | <sub>Pattern Description</sub> | <sub>Example</sub> |
| <sub>Third-Party Library</sub> | <sub>dependencies of third-party Libraries</sub> | <sub>First, converting the ReadMe text into HTML format. Then, using Xpath matches all the <li> tag under the first or second sibling node after the <h> tag that contains one of the keywords "requirement"/"dependency"/"dependencies"/"environment"/"prerequisite" Label node. Then, for the content of each <li> tag, use regular expressions to extract the Third-Party Library and its corresponding version number</sub> | <sub>### Requirements  * python 3.6  * Pytorch >= 1.0.0  * CUDA >= 9.0</sub> |
| <sub>Release Package</sub> | <sub>the release package of the current implementation</sub> | <sub></sub> |  |
| <sub>Trained Model</sub> | <sub>an instantiated ML/DL model trained using the implementation and certain dataset, which can be used directly</sub> |  |  |
| <sub>Command</sub> | <sub>commands that can be used to run the implementation</sub> |  |  |



## Resulting KG
- The resulting AI task-model KG includes 159,310 entities and 628,045
relationships. The entities include 17,250 tasks, 25,404 papers, 25,718
models, 21,003 model implementations, and 24,047 repositories. The relationships 
include 17,410 subclassOf relationships between tasks, 44,438 accomplish 
relationships, 20,594 hasEvaluation relationships, 29,281 implement relationships, 
21,008 provide relationships, 60,040 basedOn relationships, and 105,963
support relationships.

    The complete data of the resulted KG will be disclosed in case of accepted. 

## Experiments
- [RQ2: Trends of AI Tasks and Implementations Analysis.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ2/)
MLTaskKG links AI tasks, ML/DL models, and their implementations in a knowledge 
graph, thus we analyze the trends of AI tasks and their implementations. The 
analysis can help application developers to have an overview of the implementing
repositories for different AI tasks and the emergence of new ML/DL models and
implementations for specific AI tasks.

- [RQ3: AI Task-Model KG Effectiveness Evaluation.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3)
We evaluate the effectiveness of MLTaskKG by conducting a human
study. In the study we ask a set of participants to use MLTaskKG to
find suitable ML/DL libraries for given AI tasks and use 
PapersWithCode as a baseline for comparison. 
    - [ML/DL Library Retrieval Tasks.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3/Tasks.docx)
We randomly select eight questions aimed at seeking for ML/DL libraries from our
empirical study data and adapt them into eight ML/DL library retrieval tasks.
    - [Experiment Design.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3)
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

It is hereby stated that due to anonymity, some information is hidden and will be disclosed in the future.