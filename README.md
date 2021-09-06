# Replication Package of Task-Oriented ML/DL Library Recommendation based on Knowledge Graph
## Empirical Study
- [1000 ML/DL related posts.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/empirical_study/empirical_data_sample.xlsx)
This csv file contains 1000 questions randomly selected from the Stack Overflow data dump meeting all 
the criteria in the paper. In the csv file, the column “Title” represents the title of corresponding 
post, “Url” represents Stack Overflow url for posts, “Annotator_1” represents the annotation of the 
first annotator, “Annotator_2” represents the annotator of the second annotator.

- [task and factor analysis of 283 posts.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/empirical_study/empirical_data_annotation.xlsx)
This file contains 283 posts from 1000 posts which both annotators labeled true for seeking ML/DL 
libraries. In the csv file, “Title” represents the title of corresponding post, “Url” represents 
Stack Overflow url for posts, “Accepted answer” represents whether the post has accepted answer or not.
Besides, “Task” represents the task included in the post, “Task category” is the corresponding 
category of the task, “Resource type” describes whether askers first want is model or implementation, 
“Factor” represents 11 main factors contained in the post. All these four columns are arbitration of 
two annotators.

## Experiments
- [RQ1: AI Task-Model KG Intrinsic Quality Evaluation.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ1/RQ1.xlsx)
This file contains 384 relationship tuples between two entities randomly selected from AI task-model KG. 
In the csv file, “Start entity” represents the start entity of the relationship tuple, “Relation” 
represents the relationship between two entities, “End entity” represents the end entity of the 
relationship tuple, “Auxiliary” contains the information needed to judge whether the relationship 
tuple is correct or not. What’s more, “Annotator_1” represents the annotation of the first annotator, 
“Annotator_2” represents the annotator of the second annotator, both annotators need to judge the 
correctness of two entities and corresponding relationship. The last column “Arbitration” represents 
the arbitration result of two annotators.
- [RQ3: AI Task-Model KG Effectiveness Evaluation.](https://github.com/MLTaskKG/MLTaskKG.github.io/tree/main/RQ3)
We evaluate the effectiveness of MLTaskKG by conducting a human
study to find suitable ML/DL libraries for given AI tasks and use 
PapersWithCode as a baseline for comparison. 
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
completion time and plotted a box chart.

