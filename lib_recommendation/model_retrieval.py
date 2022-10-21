#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import reduce
from pathlib import Path
import html2text
import mistune
import numpy as np
import re
from gensim.models import Word2Vec
from sekg.graph.exporter.graph_data import GraphData
from data_util import DataUtil
from definitions import OUTPUT_DIR
from project.model_implementation_extraction.implementation_url_extractor import ImplementationUrlExtractor
from project.task_and_model_extraction.task_constructor import AITaskConstructor
from ast import literal_eval
import math
from collections import OrderedDict


class ModelSearcher:
    def __init__(self, graph_path):
        self.graph: GraphData = GraphData.load(graph_path)
        self.w2v_model = Word2Vec.load(str(Path(OUTPUT_DIR) / "word2vec-abstracts-100_cv_nlp"))
        self.task_2_subtask = DataUtil.load_json_dict(str(Path(OUTPUT_DIR) / "task_2_subtask.json"))
        self.alias_2_main_name = DataUtil.load_json_dict(str(Path(OUTPUT_DIR) / "alias_2_main_name.json"))
        self.task_2_vec = DataUtil.load_bin_data(str(Path(OUTPUT_DIR) / "task_2_vec.bin"))
        self.task_2_model_count = DataUtil.load_json_dict(str(Path(OUTPUT_DIR) / "task_2_model_count.json"))
        self.component_2_types = DataUtil.load_json_dict(str(Path(OUTPUT_DIR) / "component_2_types.json"))
        self.task_2_results = {}
        self.html2text = html2text.HTML2Text()
        self.html2text.ignore_links = True
        self.input_2_tasks = {}

    def search(self, task: str, topn=30):
        if task.lower() in self.alias_2_main_name:
            task = self.alias_2_main_name[task.lower()]
        else:
            task = self.get_most_similar_task(task, topn=1)[0]
        if task in self.task_2_results:
            return self.task_2_results[task]["results"], self.task_2_results[task]["filter_items"]
        task_node = self.graph.find_one_node_by_property(property_name="task", property_value=task)
        if task_node is None:
            self.task_2_results[task] = {
                "results": [],
                "filter_items": []
            }
            return [], []
        relations = self.graph.get_all_in_relations(task_node["id"])
        results = []
        filter_items = [
            {
                "name": "Hardware",
                "values": {}
            },
            {
                "name": "Language",
                "values": {}
            },
            {
                "name": "Operating System",
                "values": {}
            },
            {
                "name": "Framework",
                "values": {}
            },
            {
                "name": "Component",
                "values": {}
            },
            {
                "name": "Dataset",
                "values": {}
            }
        ]
        hardware_main_name_set = set()
        language_main_name_set = set()
        os_main_name_set = set()
        framework_main_name_set = set()
        component_type_name_set = set()
        model_nodes = []
        for startId, relationType, endId in relations:
            if relationType == "accomplish":
                model_nodes.append(self.graph.get_node_info_dict(startId))
        for model_node in model_nodes:
            implementaion_info_dict = {
                "Implementation_Name": "",
                "Model Name": model_node["properties"]["model_name"],
                "Evaluation": [],
                "Component": [],
                "Paper": [],
                "Paper Citation": 0,
                "Paper Abstract": "",
                "Dataset": [],
                "Third-Party Library": [],
                "Hardware": [],
                "Language": [],
                "Operating System": [],
                "Framework": [],
                "Repository_Name": "",
                "Repository_Url": "",
                "Star Count": 0,
                "Watch Count": 0,
                "Fork Count": 0,
                "Issue Count": 0,
                "Update Time": "",
                "License": [],
                "Readme": "",
                "Has Documents": "No",
                "Has Release Package": "No",
                "Has Guided Command": "No",
                "Has Trained Model": "No",
                "Has Example Script": "No",
                "Performance": 0,
                "Quality": 0,
                "Usability": 0
            }
            model_quality_dict = {
                "average_paper_citation_count": 0,
                "average_paper_year": 0,
                "average_evaluation_ranking": 0
            }
            citation_list = []
            year_list = []
            ranking_list = []
            model_out_relations = self.graph.get_all_out_relations(model_node["id"])
            paper_flag = True
            for startId, relationType, endId in model_out_relations:
                if relationType == "use":
                    component_node = self.graph.get_node_info_dict(endId)
                    if component_node["properties"]["component_name"] in self.component_2_types:
                        component_type_name_set.update(set(self.component_2_types[component_node["properties"]["component_name"]]))
                        implementaion_info_dict["Component"].append(component_node["properties"]["component_name"])
                elif relationType == "proposed in" and paper_flag:
                    paper_node = self.graph.get_node_info_dict(endId)
                    implementaion_info_dict["Paper"].append(paper_node["properties"]["paper_url"])
                    implementaion_info_dict["Paper Citation"] = int(paper_node["properties"]["citation_count"]) if "citation_count" in paper_node["properties"].keys() else 0
                    implementaion_info_dict["Paper Abstract"] = paper_node["properties"]["abstract"]
                    citation_list.append(int(paper_node["properties"]["citation_count"]) if "citation_count" in paper_node["properties"].keys() else 0)
                    year_list.append(int(paper_node["properties"]["year"]) if paper_node["properties"]["year"] is not None else 2010)
                    paper_flag = False
                elif relationType == "has evaluation":
                    if self.graph.exist_relation(endId, "performed for", task_node["id"]):
                        dataset_node_ids = [rel[2] for rel in self.graph.get_relations(endId, "performed on")]
                        for node_id in dataset_node_ids:
                            ranking_list.append(int(self.graph.get_node_info_dict(endId)["properties"]["rank"]))
                            implementaion_info_dict["Evaluation"].append(
                                str(self.graph.get_node_info_dict(node_id)["properties"]["dataset_name"]) + ': ' +
                                str(self.graph.get_node_info_dict(endId)["properties"]["evaluation_name"]))
                else:
                    continue
            model_quality_dict["average_paper_citation_count"] = self.get_average_for_list(citation_list)
            model_quality_dict["average_paper_year"] = self.get_average_for_list(year_list)
            model_quality_dict["average_evaluation_ranking"] = self.get_average_for_list(ranking_list)
            implementaion_info_dict["Performance"] = self.calculate_model_performance_score(model_quality_dict)
            model_in_relations = self.graph.get_all_in_relations(model_node["id"])
            model_implementation_nodes = []
            for startId, relationType, endId in model_in_relations:
                if relationType == "implement":
                    model_implementation_nodes.append(self.graph.get_node_info_dict(startId))
            for model_implementation_node in model_implementation_nodes:
                implementaion_info_dict = implementaion_info_dict.copy()
                implementaion_info_dict["Framework"] = []
                implementaion_info_dict["Dataset"] = []
                implementaion_info_dict["Third-Party Library"] = []
                implementaion_info_dict["Language"] = []
                implementaion_info_dict["Operating System"] = []
                implementaion_info_dict["Hardware"] = []
                implementaion_info_dict["Implementation_Name"] = model_implementation_node["properties"]["model_implementation_name"]
                model_implementation_in_relations = self.graph.get_all_in_relations(
                    model_implementation_node["id"])
                for startId, relationType, endId in model_implementation_in_relations:
                    if relationType == "provide":
                        repo_node = self.graph.get_node_info_dict(startId)
                        license_list = []
                        for s, r, e in self.graph.get_relations(start_id=repo_node["id"], relation_type="has license"):
                            license_list.append(self.graph.get_node_info_dict(e)["properties"]["license_name"])
                        implementaion_info_dict["Repository_Url"] = repo_node["properties"]["implementation_url"].replace("api.", "").replace("repos/", "")
                        repo_name = ImplementationUrlExtractor.get_repo_name(implementaion_info_dict["Repository_Url"])
                        implementaion_info_dict["Repository_Name"] = repo_node["properties"]["implementation_url"] if repo_name is None else repo_name
                        implementaion_info_dict["Star Count"] = repo_node["properties"]["star_count"]
                        implementaion_info_dict["Watch Count"] = repo_node["properties"]["watch_count"]
                        implementaion_info_dict["Fork Count"] = repo_node["properties"]["fork_count"]
                        implementaion_info_dict["Issue Count"] = repo_node["properties"]["issue_count"]
                        implementaion_info_dict["Update Time"] = repo_node["properties"]["update_time"].split(' ')[0].rsplit('-', 1)[0]
                        implementaion_info_dict["License"] = license_list
                        readme_html = mistune.html(repo_node["properties"]["readme"])
                        implementaion_info_dict["Readme"] = re.sub(r'\n+', '\n', re.sub(r'#+', '', self.html2text.handle(readme_html)))[:100] if readme_html is not None else ""
                        implementaion_info_dict["Has Documents"] = "No" if not literal_eval(repo_node["properties"]["doc_path"]) else "Yes"
                        trained_model_flag = "No"
                        if repo_node["properties"]["trained_model"] is not None and repo_node["properties"][
                            "trained_model"] != "":
                            if literal_eval(repo_node["properties"]["trained_model"]):
                                trained_model_flag = "Yes"
                        implementaion_info_dict["Has Trained Model"] = trained_model_flag
                        command_flag = "No"
                        if repo_node["properties"]["command"] is not None and repo_node["properties"]["command"] != "":
                            for key in literal_eval(repo_node["properties"]["command"]):
                                if literal_eval(repo_node["properties"]["command"])[key]:
                                    command_flag = "Yes"
                        implementaion_info_dict["Has Guided Command"] = command_flag
                        implementaion_info_dict["Has Example Script"] = "No" if not literal_eval(repo_node["properties"]["example_path"]) else "Yes"
                        release_flag = "No"
                        if repo_node["properties"]["release"] is not None and repo_node["properties"]["release"] != "":
                            if literal_eval(repo_node["properties"]["release"]):
                                release_flag = "Yes"
                        implementaion_info_dict["Has Release Package"] = release_flag
                        implementaion_info_dict["Quality"] = self.get_code_related_score(repo_node)[0]
                        implementaion_info_dict["Usability"] = self.get_code_related_score(repo_node)[1]
                        break
                model_implementation_out_relations = self.graph.get_all_out_relations(
                    model_implementation_node["id"])
                for startId, relationType, endId in model_implementation_out_relations:
                    if relationType == "base on":
                        framework_node = self.graph.get_node_info_dict(endId)
                        framework_main_name_set.add(framework_node["properties"]["framework_name"].replace(
                            framework_node["properties"]["version"], '').strip())
                        implementaion_info_dict["Framework"].append(framework_node["properties"]["framework_name"])
                    elif relationType == "use":
                        implementaion_info_dict["Dataset"].append(self.graph.get_node_info_dict(endId)["properties"]["dataset_name"])
                    elif relationType == "depend on":
                        implementaion_info_dict["Third-Party Library"].append(self.graph.get_node_info_dict(endId)["properties"]["library_name"])
                    elif relationType == "support":
                        end_node = self.graph.get_node_info_dict(endId)
                        if end_node["properties"]["entity_type"] == 6:
                            language_main_name_set.add(end_node["properties"]["language_version_name"].replace(
                                end_node["properties"]["version"], '').strip().split(' ')[0])
                            implementaion_info_dict["Language"].append(
                                end_node["properties"]["language_version_name"])
                        elif end_node["properties"]["entity_type"] == 10:
                            os_main_name_set.add(end_node["properties"]["operation_system_name"].replace(
                                end_node["properties"]["version"], '').strip())
                            implementaion_info_dict["Operating System"].append(
                                end_node["properties"]["operation_system_name"])
                        elif end_node["properties"]["entity_type"] == 11:
                            hardware_main_name_set.add(end_node["properties"]["hardware_name"].replace(
                                end_node["properties"]["version"], '').strip())
                            implementaion_info_dict["Hardware"].append(end_node["properties"]["hardware_name"])
                    else:
                        continue
                implementaion_info_dict["Evaluation"] = list(set(implementaion_info_dict["Evaluation"]))
                implementaion_info_dict["Component"] = list(set(implementaion_info_dict["Component"]))
                implementaion_info_dict["Paper"] = list(set(implementaion_info_dict["Paper"]))
                implementaion_info_dict["Dataset"] = list(set(implementaion_info_dict["Dataset"]))
                implementaion_info_dict["Third-Party Library"] = list(set(implementaion_info_dict["Third-Party Library"]))
                implementaion_info_dict["Hardware"] = list(set(implementaion_info_dict["Hardware"]))
                implementaion_info_dict["Language"] = list(set(implementaion_info_dict["Language"]))
                implementaion_info_dict["Operating System"] = list(set(implementaion_info_dict["Operating System"]))
                implementaion_info_dict["Framework"] = list(set(implementaion_info_dict["Framework"]))
                implementaion_info_dict["License"] = list(set(implementaion_info_dict["License"]))
                results.append(implementaion_info_dict)

        for hardware_main_name in hardware_main_name_set:
            filter_items[0]["values"][hardware_main_name] = []
        for language_main_name in language_main_name_set:
            filter_items[1]["values"][language_main_name] = []
        for os_main_name in os_main_name_set:
            filter_items[2]["values"][os_main_name] = []
        for framework_main_name in framework_main_name_set:
            filter_items[3]["values"][framework_main_name] = []
        for component_type_name in component_type_name_set:
            filter_items[4]["values"][component_type_name] = []
        for result in results:
            for hardware in result["Hardware"]:
                for hardware_main_name in filter_items[0]["values"].keys():
                    if hardware.startswith(hardware_main_name):
                        filter_items[0]["values"][hardware_main_name].append(hardware)
            for language in result["Language"]:
                for language_main_name in filter_items[1]["values"].keys():
                    if language.startswith(language_main_name):
                        filter_items[1]["values"][language_main_name].append(language)
            for os in result["Operating System"]:
                for os_main_name in filter_items[2]["values"].keys():
                    if os.startswith(os_main_name):
                        filter_items[2]["values"][os_main_name].append(os)
            for framework in result["Framework"]:
                for framework_main_name in filter_items[3]["values"].keys():
                    if framework.startswith(framework_main_name):
                        filter_items[3]["values"][framework_main_name].append(framework)
            for component in result["Component"]:
                for component_type in self.component_2_types[component]:
                    filter_items[4]["values"][component_type].append(component)
            for dataset in result["Dataset"]:
                if dataset not in filter_items[5]["values"].keys():
                    filter_items[5]["values"][dataset] = []
                    filter_items[5]["values"][dataset].append(dataset)
        for item in filter_items.copy():
            if not item["values"]:
                filter_items.remove(item)
            for key in item["values"]:
                item["values"][key] = list(set(item["values"][key]))
        results = self.remove_duplicate_dict_array(results)
        self.task_2_results[task] = {
            "results": results,
            "filter_items": filter_items
        }
        return results, filter_items

    @staticmethod
    def get_average_for_list(l):
        if not l:
            return 0
        return float(sum(l) / len(l))

    def get_code_related_score(self, repo_node):
        release_flag = 0
        if repo_node["properties"]["release"] is not None and repo_node["properties"]["release"] != "":
            if literal_eval(repo_node["properties"]["release"]):
                release_flag = 1

        code_quality_dict = {
            "star_count": repo_node["properties"]["star_count"],
            "watch_count": repo_node["properties"]["watch_count"],
            "fork_count": repo_node["properties"]["fork_count"],
            "issue_count": repo_node["properties"]["issue_count"],
            "homepage_url": 0 if repo_node["properties"]["homepage_url"] == "" else 1,
            "release": release_flag,
            "update_time": repo_node["properties"]["update_time"],
            "code_encapsulation_degree": repo_node["properties"]["rating"],
            "library_count": len(self.graph.get_relations(start_id=repo_node["id"], relation_type="depend on")),
            "test_code": 0 if repo_node["properties"]["provide_test"] == "false" else 1
        }
        command_flag = 0
        if repo_node["properties"]["command"] is not None and repo_node["properties"]["command"] != "":
            for key in literal_eval(repo_node["properties"]["command"]):
                if literal_eval(repo_node["properties"]["command"])[key]:
                    command_flag = 1
        trained_model_flag = 0
        if repo_node["properties"]["trained_model"] is not None and repo_node["properties"]["trained_model"] != "":
            if literal_eval(repo_node["properties"]["trained_model"]):
                trained_model_flag = 1
        code_usability_dict = {
            "trained_model": trained_model_flag,
            "documents": 0 if repo_node["properties"]["provide_doc"] == "false" else 1,
            "homepage_url": 0 if repo_node["properties"]["homepage_url"] == "" else 1,
            "release": release_flag,
            "command": command_flag,
            "example": 0 if repo_node["properties"]["provide_example"] == "false" else 1
        }
        return self.calculate_code_quality_score(code_quality_dict), self.calculate_code_usability_score(code_usability_dict)

    def calculate_model_performance_score(self, model_quality_dict):
        normalization_citation = float(math.log(model_quality_dict["average_paper_citation_count"]) / math.log(82578)) if model_quality_dict["average_paper_citation_count"] != 0 else 0
        normalization_year = float((model_quality_dict["average_paper_year"] - 2010) / 10)
        normalization_ranking = float(1 / model_quality_dict["average_evaluation_ranking"]) if model_quality_dict["average_evaluation_ranking"] != 0 else 0
        return round(float((normalization_citation + normalization_year + normalization_ranking) / 3), 2)

    def calculate_code_quality_score(self, code_quality_dict):
        normalization_star_count = float(math.log(code_quality_dict["star_count"]) / math.log(157775)) if code_quality_dict["star_count"] != 0 else 0
        normalization_watch_count = float(math.log(code_quality_dict["watch_count"]) / math.log(157775)) if code_quality_dict["watch_count"] != 0 else 0
        normalization_fork_count = float(math.log(code_quality_dict["fork_count"]) / math.log(85202)) if code_quality_dict["fork_count"] != 0 else 0
        normalization_issue_count = float(math.log(code_quality_dict["issue_count"]) / math.log(9380)) if code_quality_dict["issue_count"] != 0 else 0
        normalization_homepage_url = float(code_quality_dict["homepage_url"])
        normalization_release = float(code_quality_dict["release"])
        normalization_update_time = float((int(code_quality_dict["update_time"].split('-')[0]) - 2014) / 7) if int(code_quality_dict["update_time"].split('-')[0]) != 1 else 0
        normalization_code_encapsulation_degree = float((code_quality_dict["code_encapsulation_degree"] - 1) / 4)
        normalization_library_count = float(math.log(code_quality_dict["library_count"]) / math.log(588)) if code_quality_dict["library_count"] != 0 else 0
        normalization_test_code = float(code_quality_dict["test_code"])
        return round(float((normalization_star_count + normalization_watch_count + normalization_fork_count +
                     normalization_issue_count + normalization_homepage_url + normalization_release +
                     normalization_update_time + normalization_code_encapsulation_degree + normalization_library_count +
                     normalization_test_code)
                     / 10), 2)

    def calculate_code_usability_score(self, code_usability_dict):
        normalization_trained_model = float(code_usability_dict["trained_model"])
        normalization_documents = float(code_usability_dict["documents"])
        normalization_homepage_url = float(code_usability_dict["homepage_url"])
        normalization_release = float(code_usability_dict["release"])
        normalization_command = float(code_usability_dict["command"])
        normalization_example = float(code_usability_dict["example"])
        return round(float((normalization_trained_model + normalization_documents + normalization_homepage_url +
                      normalization_release + normalization_command + normalization_example) / 6), 2)

    def filter(self, task, filter_dict: dict):
        results = []
        if task.lower() in self.alias_2_main_name:
            task = self.alias_2_main_name[task.lower()]
        else:
            task = self.get_most_similar_task(task, topn=1)[0]
        for result in self.task_2_results[task]["results"]:
            flag = True
            for filter_key in filter_dict.keys():
                if not set(result[filter_key]) & set(filter_dict[filter_key]):
                    flag = False
                    break
            if flag:
                results.append(result)
        results = self.remove_duplicate_dict_array(results)
        return results

    def suggest_task(self, input_entry: str, topn=5):
        if input_entry in self.input_2_tasks:
            return self.input_2_tasks[input_entry]
        task_dict = OrderedDict()
        tasks = []
        subtasks = []
        related_tasks = []
        for alias in self.alias_2_main_name:
            if set(input_entry.lower().split(' ')).issubset(set(alias.split(' '))):
                if self.task_2_model_count[self.alias_2_main_name[alias]] > 0:
                    tasks.append(self.alias_2_main_name[alias])
        if input_entry.lower() in self.alias_2_main_name:
            if self.alias_2_main_name[input_entry.lower()] in self.task_2_subtask.keys():
                subtasks = self.task_2_subtask[self.alias_2_main_name[input_entry.lower()]]
        related_tasks.extend(self.get_most_similar_task(input_entry, topn=200))
        task_dict["Tasks"] = tasks[:10]
        tmp_subtasks = []
        for subtask in subtasks:
            if self.task_2_model_count[subtask] > 0:
                tmp_subtasks.append(subtask)
        task_dict["Subtasks"] = tmp_subtasks[:5]
        tmp_related_tasks = []
        for related_task in related_tasks:
            if self.task_2_model_count[related_task] > 0:
                tmp_related_tasks.append(related_task)
        task_dict["Related Tasks"] = tmp_related_tasks[:5]
        self.input_2_tasks[input_entry] = task_dict
        return task_dict

    def get_most_similar_task(self, task, topn=5):
        most_similar_tasks = []
        sims = self.w2v_model.wv.cosine_similarities(AITaskConstructor.get_avg_w2v_vec(task, self.w2v_model),
                                                     np.array(list(self.task_2_vec.values())))
        sims_list = np.nan_to_num(sims).tolist()
        sort_sims = sorted(enumerate(sims_list), key=lambda item: -item[1])
        for index in range(topn):
            most_similar_tasks.append(list(self.task_2_vec.keys())[sort_sims[index][0]])
        return most_similar_tasks

    @staticmethod
    def remove_duplicate_dict_array(data):
        func = lambda x, y: x + [y] if y not in x else x
        data = reduce(func, [[], ] + data)
        return data
