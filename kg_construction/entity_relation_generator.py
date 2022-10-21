#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from pathlib import Path
import gzip
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ast import literal_eval
from data_util import DataUtil
from definitions import OUTPUT_DIR, DATA_DIR, ROOT_DIR
from project.kg_construction.entity_relation_category import RelationCategory
from project.model_implementation_extraction.implementation_info_extractor import PatternInfoExtractor
from project.model_implementation_extraction.implementation_url_extractor import ImplementationUrlExtractor
from project.task_and_model_extraction.task_constructor import AITaskConstructor
from script.database.AI_Paper_Model import AIPaperModel
from script.database.AI_Task_Model import AITaskModel
from script.database.Implementation_Model import ImplementationModel
from project.model_implementation_extraction.implementation_info_extractor import FRAMEWORK


class EntityRelationGenerator:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:123456@10.176.64.33/AIKG?charset=utf8mb4")
        self.session = None
        self.relation_str_to_code = RelationCategory.str_to_category_code()
        self.FRAMEWORK_LOWER = {value: key for key, value in FRAMEWORK.items()}
        self.title2id = {}
        self.model_name_set = set()
        self.implementation_id_2_model_name = DataUtil.load_json_array(str(Path(OUTPUT_DIR) / "implementation_id_2_model_name.json"))
        self.init_operation()
        self.MAX_PAPER_ID = 90000
        self.relation_list = []
        self.paper_entity_list = []
        self.task_entity_list = []
        self.model_entity_list = []
        self.repository_entity_list = []
        self.model_implementation_entity_list = []
        self.license_entity_list = []
        self.language_version_entity_list = []
        self.framework_entity_list = []
        self.third_party_library_entity_list = []
        self.dataset_entity_list = []
        self.hardware_entity_list = []
        self.operation_system_entity_list = []
        self.component_entity_list = []
        self.component_category_entity_list = []
        self.evaluation_entity_list = []
        self.computing_platform_entity_list = []
        self.tmp_framework_entity_set = set()
        self.tmp_hardware_entity_set = set()
        self.tmp_language_version_entity_set = set()
        self.tmp_operation_system_entity_set = set()

    def init_operation(self):
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()
        paper_id_title_list = DataUtil.load_json_array(str(Path(DATA_DIR) / "paper_id_title.json"))
        for item in paper_id_title_list:
            self.title2id[item["title"].strip('.').lower()] = item["id"]

    def generate_entity_relation(self):
        self.generate_task_entity_from_structure()
        self.generate_paper_entity()
        self.generate_dataset_entity()
        self.generate_artificial_entity_relation()
        self.generate_model_related_entity_relation()
        self.generate_component_related_entity_relation()
        self.generate_implementation_related_entity_relation()
        self.generate_evaluation_related_entity_relation()
        DataUtil.save_json_array(data=self.dataset_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/dataset_entity.json"))
        DataUtil.save_json_array(data=self.task_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/task_entity.json"))
        DataUtil.save_json_array(data=self.paper_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/paper_entity.json"))
        DataUtil.save_json_array(data=list(self.model_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/model_entity.json"))
        DataUtil.save_json_array(data=self.relation_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/relation.json"))
        DataUtil.save_json_array(data=list(self.model_implementation_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/model_implementation_entity.json"))
        DataUtil.save_json_array(data=self.computing_platform_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/computing_platform_entity.json"))
        DataUtil.save_json_array(data=self.component_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/component_entity.json"))
        DataUtil.save_json_array(data=self.component_category_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/component_category_entity.json"))
        DataUtil.save_json_array(data=self.evaluation_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/evaluation_entity.json"))
        DataUtil.save_json_array(data=self.repository_entity_list,
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/repository_entity.json"))
        DataUtil.save_json_array(data=list(self.license_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/license_entity.json"))
        DataUtil.save_json_array(data=list(self.language_version_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/language_version_entity.json"))
        DataUtil.save_json_array(data=list(self.framework_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/framework_entity.json"))
        DataUtil.save_json_array(data=list(self.third_party_library_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/third_party_library_entity.json"))
        DataUtil.save_json_array(data=list(self.hardware_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/hardware_entity.json"))
        DataUtil.save_json_array(data=list(self.operation_system_entity_list),
                                 path=str(Path(OUTPUT_DIR) / "entity_relation_data/operation_system_entity.json"))

    def generate_task_entity_from_structure(self):
        print("start generate task entity")
        task_structure_path = str(Path(OUTPUT_DIR) / "complemented_task_structure_cv_nlp.json")
        task_structure = DataUtil.load_json_array(task_structure_path)
        for level_1_task in task_structure:
            self.task_entity_list.append({
                "task": level_1_task["task"],
                "descriptions": level_1_task["descriptions"],
                "aliases": level_1_task["aliases"]
            })
            self.add_subtask(level_1_task)
        print("end generate task entity")

    def add_subtask(self, parent_task):
        for subtask in parent_task["subtasks"]:
            self.task_entity_list.append({
                "task": subtask["task"],
                "descriptions": subtask["descriptions"],
                "aliases": subtask["aliases"]
            })
            self.relation_list.append(
                {"end_name": subtask["task"], "relation_type": 3, "start_name": parent_task["task"]})
            self.add_subtask(subtask)

    def generate_paper_entity(self):
        print("start generate paper entity")
        paper_ids = AIPaperModel.get_data_ids(self.session)
        for paper_id in paper_ids:
            paper_data = AIPaperModel.get_data_object_by_id(paper_id, self.session)
            self.paper_entity_list.append({
                "paper_id": paper_id.Id,
                "title": paper_data.Title,
                "author": paper_data.Author,
                "abstract": paper_data.Abstract,
                "keyword": paper_data.Keyword,
                "conference": paper_data.Conference,
                "year": paper_data.Year,
                "paper_url": paper_data.Paper_Url,
                "pdf_url": paper_data.PDF_Url,
                "citation_count": paper_data.Citation_Count
            })
        print("end generate paper entity")

    def generate_dataset_entity(self):
        print("start generate dataset entity")
        with gzip.open(str(Path(DATA_DIR) / "datasets.json.gz"), 'rt', encoding='UTF-8') as f:
            json_list = json.load(f)
        for item in json_list:
            alias_name_set = set()
            if item["name"] != "" and item["name"] is not None:
                alias_name_set.add(item["name"])
                if item["full_name"] != "" and item["full_name"] is not None:
                    alias_name_set.add(item["full_name"])
                if item["variants"]:
                    alias_name_set.update(set(item["variants"]))
                self.dataset_entity_list.append({
                    "dataset_name": item["name"],
                    "aliases": list(alias_name_set),
                    "description": item["description"]
                })
        print("end generate dataset entity")

    def generate_artificial_entity_relation(self):
        print("start generate artificial entity")
        framework_entity_relation = DataUtil.load_json_dict(str(Path(ROOT_DIR) / "background_knowledge/ai_framework.json"))
        hardware_entity_relation = DataUtil.load_json_dict(str(Path(ROOT_DIR) / "background_knowledge/hardware.json"))
        language_entity_relation = DataUtil.load_json_dict(str(Path(ROOT_DIR) / "background_knowledge/language.json"))
        operation_system_entity_relation = DataUtil.load_json_dict(str(Path(ROOT_DIR) / "background_knowledge/operation_system.json"))
        platform_entity_relation = DataUtil.load_json_dict(str(Path(ROOT_DIR) / "background_knowledge/platform.json"))
        for entity in framework_entity_relation["entities"]:
            self.framework_entity_list.append({
                "framework_name": entity["name"],
                "description": entity["description"],
                "aliases": entity["aliases"],
                "version": entity["version"]
            })
            self.tmp_framework_entity_set.add(entity["name"])
        for relation in framework_entity_relation["relations"]:
            for start_entity in relation["start_entities"]:
                for end_entity in relation["end_entities"]:
                    self.relation_list.append(
                        {"end_name": end_entity, "relation_type": self.relation_str_to_code[relation["relation_type"]],
                         "start_name": start_entity})

        for entity in hardware_entity_relation["entities"]:
            self.hardware_entity_list.append({
                "hardware_name": entity["name"],
                "description": entity["description"],
                "aliases": entity["aliases"],
                "version": entity["version"]
            })
            self.tmp_hardware_entity_set.add(entity["name"])
        for relation in hardware_entity_relation["relations"]:
            for start_entity in relation["start_entities"]:
                for end_entity in relation["end_entities"]:
                    self.relation_list.append(
                        {"end_name": end_entity, "relation_type": self.relation_str_to_code[relation["relation_type"]],
                         "start_name": start_entity})

        for entity in language_entity_relation["entities"]:
            self.language_version_entity_list.append({
                "language_version_name": entity["name"],
                "description": entity["description"],
                "aliases": entity["aliases"],
                "version": entity["version"]
            })
            self.tmp_language_version_entity_set.add(entity["name"])
        for relation in language_entity_relation["relations"]:
            for start_entity in relation["start_entities"]:
                for end_entity in relation["end_entities"]:
                    self.relation_list.append(
                        {"end_name": end_entity, "relation_type": self.relation_str_to_code[relation["relation_type"]],
                         "start_name": start_entity})

        for entity in operation_system_entity_relation["entities"]:
            self.operation_system_entity_list.append({
                "operation_system_name": entity["name"],
                "description": entity["description"],
                "aliases": entity["aliases"],
                "version": entity["version"]
            })
            self.tmp_operation_system_entity_set.add(entity["name"])
        for relation in operation_system_entity_relation["relations"]:
            for start_entity in relation["start_entities"]:
                for end_entity in relation["end_entities"]:
                    self.relation_list.append(
                        {"end_name": end_entity, "relation_type": self.relation_str_to_code[relation["relation_type"]],
                         "start_name": start_entity})

        for entity in platform_entity_relation["entities"]:
            self.computing_platform_entity_list.append({
                "computing_platform_name": entity["name"],
                "description": entity["description"],
                "aliases": entity["aliases"],
                "version": entity["version"]
            })
        for relation in platform_entity_relation["relations"]:
            for start_entity in relation["start_entities"]:
                for end_entity in relation["end_entities"]:
                    self.relation_list.append(
                        {"end_name": end_entity, "relation_type": self.relation_str_to_code[relation["relation_type"]],
                         "start_name": start_entity})
        print("end generate artificial entity")

    def generate_implementation_related_entity_relation(self):
        print("start generate implementation related entity")
        tmp_license_entity_set = set()
        tmp_third_party_library_entity_set = set()
        paper_repo_info_dict = DataUtil.load_json_dict(path=str(Path(DATA_DIR) / "paper_repo_info.json"))
        awesome_repo_info_dict = DataUtil.load_json_dict(path=str(Path(DATA_DIR) / "awesome_repo_info.json"))
        implementation_ids = ImplementationModel.get_data_ids(self.session)
        for implementation_id in implementation_ids:
            implementation_data = ImplementationModel.get_data_object_by_id(implementation_id, self.session)
            if implementation_data is not None:
                repo_info = {}
                model_implementation_list = []
                if str(implementation_id.Id) in paper_repo_info_dict:
                    repo_info = paper_repo_info_dict[str(implementation_id.Id)]
                    models = repo_info["models"].keys()
                    for model in repo_info["models"]:
                        file_online_path = repo_info["models"][model]["file_online_path"]
                        if "github.com" not in file_online_path:
                            model_implementation = implementation_data.Implementation_Url
                        else:
                            model_implementation = file_online_path
                        model_implementation_list.append(model_implementation)
                        self.model_implementation_entity_list.append({"model_implementation_name": model_implementation})
                        self.relation_list.append(
                            {"end_name": model_implementation, "relation_type": 4,
                             "start_name": implementation_data.Id})
                        if str(implementation_id.Id) in self.implementation_id_2_model_name:
                            self.relation_list.append(
                                {"end_name": self.implementation_id_2_model_name[str(implementation_id.Id)],
                                 "relation_type": 11,
                                 "start_name": model_implementation})
                        else:
                            self.relation_list.append(
                                {"end_name": model,
                                 "relation_type": 11,
                                 "start_name": model_implementation})
                        methods = repo_info["models"][model]["methods"]
                        if methods:
                            method_list = methods["self defined methods"]
                            method_list.extend(methods["AI framework methods"])
                            for method in method_list:
                                if str(implementation_id.Id) in self.implementation_id_2_model_name:
                                    self.relation_list.append(
                                        {"end_name": method, "relation_type": 8,
                                         "start_name": self.implementation_id_2_model_name[str(implementation_id.Id)]})
                            if methods["AI framework"] != "" and methods["AI framework"] in self.FRAMEWORK_LOWER.keys():
                                if self.FRAMEWORK_LOWER[methods["AI framework"]] not in self.tmp_framework_entity_set:
                                    self.tmp_framework_entity_set.add(self.FRAMEWORK_LOWER[methods["AI framework"]])
                                    self.framework_entity_list.append({
                                        "framework_name": self.FRAMEWORK_LOWER[methods["AI framework"]],
                                        "description": "",
                                        "aliases": [],
                                        "version": ""
                                    })
                                self.relation_list.append(
                                    {"end_name": self.FRAMEWORK_LOWER[methods["AI framework"]],
                                     "relation_type": 5, "start_name": model_implementation})
                                for method in methods["AI framework methods"]:
                                    self.relation_list.append(
                                        {"end_name": method, "relation_type": 11,
                                         "start_name": self.FRAMEWORK_LOWER[methods["AI framework"]]}
                                    )
                elif str(implementation_id.Id) in awesome_repo_info_dict:
                    repo_info = awesome_repo_info_dict[str(implementation_id.Id)]
                    tasks = repo_info["tasks"].keys()
                    papers = repo_info["papers"]
                    models = repo_info["models"].keys()
                    for model in repo_info["models"]:
                        if model not in self.model_name_set:
                            self.model_name_set.add(model)
                            self.model_entity_list.append({
                                "model_name": model,
                                "alias": "",
                                "extraction_source": 2,
                                "model_speed": ""
                            })
                        file_online_path = repo_info["models"][model]["file_online_path"]
                        if "github.com" not in file_online_path:
                            model_implementation = implementation_data.Implementation_Url
                        else:
                            model_implementation = file_online_path
                        model_implementation_list.append(model_implementation)
                        self.model_implementation_entity_list.append({"model_implementation_name": model_implementation})
                        self.relation_list.append(
                            {"end_name": model_implementation, "relation_type": 4,
                             "start_name": implementation_data.Id})
                        self.relation_list.append(
                            {"end_name": model,
                             "relation_type": 11,
                             "start_name": model_implementation})
                        methods = repo_info["models"][model]["methods"]
                        if methods:
                            method_list = methods["self defined methods"]
                            method_list.extend(methods["AI framework methods"])
                            for method in method_list:
                                self.relation_list.append(
                                    {"end_name": method, "relation_type": 8, "start_name": model})
                            if methods["AI framework"] != "" and methods["AI framework"] in self.FRAMEWORK_LOWER.keys():
                                if self.FRAMEWORK_LOWER[methods["AI framework"]] not in self.tmp_framework_entity_set:
                                    self.tmp_framework_entity_set.add(self.FRAMEWORK_LOWER[methods["AI framework"]])
                                    self.framework_entity_list.append({
                                        "framework_name": self.FRAMEWORK_LOWER[methods["AI framework"]],
                                        "description": "",
                                        "aliases": [],
                                        "version": ""
                                    })
                                self.relation_list.append(
                                    {"end_name": self.FRAMEWORK_LOWER[methods["AI framework"]],
                                     "relation_type": 5, "start_name": model_implementation})
                                for method in methods["AI framework methods"]:
                                    self.relation_list.append(
                                        {"end_name": method, "relation_type": 11,
                                         "start_name": self.FRAMEWORK_LOWER[methods["AI framework"]]}
                                    )
                    for task in tasks:
                        self.relation_list.append(
                            {"end_name": task, "relation_type": 17, "start_name": implementation_id.Id})
                    for model in models:
                        for paper in papers:
                            if paper.lower() in self.title2id:
                                self.relation_list.append(
                                    {"end_name": self.title2id[paper.lower()], "relation_type": 17, "start_name": model})
                else:
                    repo_info = {
                        "rating": 0,
                        "structure": {
                            "provide dataset": "false",
                            "dataset path": [],
                            "provide doc": "false",
                            "doc path": [],
                            "provide example": "false",
                            "example path": [],
                            "provide test": "false",
                            "test path": []
                        }
                    }
                model_implementation_list.append(implementation_data.Id)
                self.repository_entity_list.append({
                    "implementation_id": implementation_data.Id,
                    "implementation_url": implementation_data.Implementation_Url,
                    "watch_count": implementation_data.Watch_Count,
                    "star_count": implementation_data.Star_Count,
                    "fork_count": implementation_data.Fork_Count,
                    "issue_count": implementation_data.Issue_Count,
                    "about": implementation_data.About,
                    "topic": implementation_data.Topic,
                    "readme": implementation_data.Readme,
                    "update_time": str(implementation_data.Update_Time),
                    "homepage_url": implementation_data.Homepage_Url,
                    "trained_model": implementation_data.Trained_Model,
                    "command": implementation_data.Command,
                    "release": implementation_data.Release,
                    "rating": repo_info["rating"],
                    "dataset_path": str(repo_info["structure"]["dataset path"]),
                    "doc_path": str(repo_info["structure"]["doc path"]),
                    "example_path": str(repo_info["structure"]["example path"]),
                    "test_path": str(repo_info["structure"]["test path"]),
                    "provide_dataset": str(repo_info["structure"]["provide dataset"]),
                    "provide_doc": str(repo_info["structure"]["provide doc"]),
                    "provide_example": str(repo_info["structure"]["provide example"]),
                    "provide_test": str(repo_info["structure"]["provide test"])
                })
                if implementation_data.License != "":
                    if implementation_data.License not in tmp_license_entity_set:
                        tmp_license_entity_set.add(implementation_data.License)
                        self.license_entity_list.append({"license_name": implementation_data.License})
                    self.relation_list.append({"end_name": implementation_data.License, "relation_type": 10,
                                               "start_name": implementation_data.Id})

                for model_implementation in model_implementation_list:
                    if implementation_data.Language_Version != "" and implementation_data.Language_Version is not None:
                        for language, version in literal_eval(implementation_data.Language_Version):
                            if language is None:
                                continue
                            version = version.strip('.')
                            if self.Upper_first_letter(language) in self.tmp_language_version_entity_set and version != "":
                                self.relation_list.append({"end_name": self.Upper_first_letter(language) + ' ' + version,
                                                           "relation_type": 18, "start_name": self.Upper_first_letter(language)})
                            if str(self.Upper_first_letter(language) + ' ' + version).strip() not in self.tmp_language_version_entity_set:
                                self.tmp_language_version_entity_set.add(str(self.Upper_first_letter(language) + ' ' + version).strip())
                                self.language_version_entity_list.append({
                                    "language_version_name": str(self.Upper_first_letter(language) + ' ' + version).strip(),
                                    "description": "",
                                    "aliases": [],
                                    "version": version
                                })
                            self.relation_list.append({"end_name": str(self.Upper_first_letter(language) + ' ' + version).strip(),
                                                       "relation_type": 7, "start_name": model_implementation})
                    if implementation_data.Framework != "":
                        for framework, version in literal_eval(implementation_data.Framework):
                            version = version.strip('.')
                            if self.Upper_first_letter(framework) in self.tmp_framework_entity_set and version != "":
                                self.relation_list.append({"end_name": self.Upper_first_letter(framework) + ' ' + version,
                                                           "relation_type": 18, "start_name": self.Upper_first_letter(framework)})
                            if str(self.Upper_first_letter(framework) + ' ' + version).strip() not in self.tmp_framework_entity_set:
                                self.tmp_framework_entity_set.add(str(self.Upper_first_letter(framework) + ' ' + version).strip())
                                self.framework_entity_list.append({
                                    "framework_name": str(self.Upper_first_letter(framework) + ' ' + version).strip(),
                                    "description": "",
                                    "aliases": [],
                                    "version": version
                                })
                            self.relation_list.append({"end_name": str(self.Upper_first_letter(framework) + ' ' + version).strip(),
                                                       "relation_type": 5, "start_name": model_implementation})
                    if implementation_data.Third_Party_Library != "":
                        for library, version in literal_eval(implementation_data.Third_Party_Library):
                            version = version.strip('.')
                            if self.Upper_first_letter(library) not in tmp_third_party_library_entity_set:
                                tmp_third_party_library_entity_set.add(self.Upper_first_letter(library))
                                self.third_party_library_entity_list.append({
                                    "library_name": self.Upper_first_letter(library),
                                    "description": "",
                                    "aliases": [],
                                    "version": ""
                                })
                            if self.Upper_first_letter(library) in tmp_third_party_library_entity_set and version != "":
                                self.relation_list.append({"end_name": self.Upper_first_letter(library) + ' ' + version,
                                                           "relation_type": 18, "start_name": self.Upper_first_letter(library)})
                            if str(self.Upper_first_letter(library) + ' ' + version).strip() not in tmp_third_party_library_entity_set:
                                tmp_third_party_library_entity_set.add(str(self.Upper_first_letter(library) + ' ' + version).strip())
                                self.third_party_library_entity_list.append({
                                    "library_name": str(self.Upper_first_letter(library) + ' ' + version).strip(),
                                    "description": "",
                                    "aliases": [],
                                    "version": version
                                })
                            self.relation_list.append({"end_name": str(self.Upper_first_letter(library) + ' ' + version).strip(),
                                                       "relation_type": 9, "start_name": model_implementation})
                    if implementation_data.Hardware_Device != "":
                        for hardware, version in literal_eval(implementation_data.Hardware_Device):
                            version = version.strip('.')
                            if self.Upper_first_letter(hardware) in self.tmp_hardware_entity_set and version != "":
                                self.relation_list.append({"end_name": self.Upper_first_letter(hardware) + ' ' + version,
                                                           "relation_type": 18, "start_name": self.Upper_first_letter(hardware)})
                            if str(self.Upper_first_letter(hardware) + ' ' + version).strip() not in self.tmp_hardware_entity_set:
                                self.tmp_hardware_entity_set.add(str(self.Upper_first_letter(hardware) + ' ' + version).strip())
                                self.hardware_entity_list.append({
                                    "hardware_name": str(self.Upper_first_letter(hardware) + ' ' + version).strip(),
                                    "description": "",
                                    "aliases": [],
                                    "version": version
                                })
                            self.relation_list.append({"end_name": str(self.Upper_first_letter(hardware) + ' ' + version).strip(),
                                                       "relation_type": 7, "start_name": model_implementation})
                    if implementation_data.Operation_System != "":
                        for os, version in literal_eval(implementation_data.Operation_System):
                            version = version.strip('.')
                            if self.Upper_first_letter(os) in self.tmp_operation_system_entity_set and version != "":
                                self.relation_list.append({"end_name": self.Upper_first_letter(os) + ' ' + version,
                                                           "relation_type": 18, "start_name": self.Upper_first_letter(os)})
                            if str(self.Upper_first_letter(os) + ' ' + version).strip() not in self.tmp_operation_system_entity_set:
                                self.tmp_operation_system_entity_set.add(str(self.Upper_first_letter(os) + ' ' + version).strip())
                                self.operation_system_entity_list.append({
                                    "operation_system_name": str(self.Upper_first_letter(os) + ' ' + version).strip(),
                                    "description": "",
                                    "aliases": [],
                                    "version": version
                                })
                            self.relation_list.append({"end_name": str(self.Upper_first_letter(os) + ' ' + version).strip(),
                                                       "relation_type": 7, "start_name": model_implementation})
                    if implementation_data.Dataset != "":
                        for dataset in literal_eval(implementation_data.Dataset):
                            self.relation_list.append({"end_name": dataset, "relation_type": 8,
                                                       "start_name": model_implementation})
        print("end generate implementation related entity")

    def generate_model_related_entity_relation(self):
        print("start generate model related entity and relation")
        paper_implementation_map = {}
        implementation_id_2_paper_id = DataUtil.load_json_array(str(Path(DATA_DIR) / "implementation_id_2_paper_id.json"))
        for item in implementation_id_2_paper_id:
            if item["paper_id"] not in paper_implementation_map:
                paper_implementation_map[item["paper_id"]] = []
            paper_implementation_map[item["paper_id"]].append(item["id"])
        paper_ids = AIPaperModel.get_data_ids(self.session)
        for paper_id in paper_ids:
            task_model_data = AITaskModel.get_data_object_by_id(paper_id, self.session)
            if task_model_data is not None:
                model = task_model_data.Model
                task_list = task_model_data.New_Task
                if model == "":
                    model = "Model_" + str(task_model_data.Paper_Id)
                if model not in self.model_name_set:
                    self.model_name_set.add(model)
                    if task_model_data.Model_Alias != "":
                        self.model_name_set.add(task_model_data.Model_Alias)
                    self.model_entity_list.append({
                        "model_name": model,
                        "alias": task_model_data.Model_Alias,
                        "extraction_source": 0,
                        "model_speed": task_model_data.Model_Speed
                    })
                self.relation_list.append(
                    {"end_name": paper_id.Id, "relation_type": 1, "start_name": model})
                for task in literal_eval(task_list):
                    if task != "":
                        self.relation_list.append(
                            {"end_name": task, "relation_type": 2, "start_name": model})
                        if paper_id.Id in paper_implementation_map:
                            for implementation_id in paper_implementation_map[paper_id.Id]:
                                self.relation_list.append(
                                    {"end_name": task, "relation_type": 17, "start_name": implementation_id})
        print("end generate model related entity and relation")

    def generate_component_related_entity_relation(self):
        print("start generate component related entity and relation")
        title2id = {}
        punctuation = r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""
        paper_id_title_list = DataUtil.load_json_array(str(Path(DATA_DIR) / "paper_id_title.json"))
        for item in paper_id_title_list:
            title = ''.join(ch for ch in item["title"] if ch not in punctuation).replace(' ', '-')
            title2id[title] = item["id"]
        tmp_component_entity_set = set()
        tmp_component_category_entity_set = set()
        with gzip.open(str(Path(DATA_DIR) / "methods.json.gz"), 'rt', encoding='UTF-8') as f:
            json_list = json.load(f)
        for item in json_list:
            if item["full_name"] != "":
                if item["full_name"] not in tmp_component_entity_set:
                    tmp_component_entity_set.add(item["full_name"])
                    self.component_entity_list.append({
                        "component_name": item["full_name"],
                        "alias": item["name"],
                        "description": item["description"]
                    })
                if item["paper"] != "":
                    if item["paper"] not in title2id:
                        title2id[item["paper"]] = self.MAX_PAPER_ID
                        self.paper_entity_list.append({
                            "paper_id": self.MAX_PAPER_ID,
                            "title": item["paper"],
                            "author": "",
                            "abstract": "",
                            "keyword": "",
                            "conference": "",
                            "year": None,
                            "paper_url": "",
                            "pdf_url": ""
                        })
                        self.MAX_PAPER_ID += 1
                    self.relation_list.append(
                        {"end_name": title2id[item["paper"]], "relation_type": 1, "start_name": item["full_name"]})
                for collection in item["collections"]:
                    if collection["collection"] not in tmp_component_category_entity_set:
                        tmp_component_category_entity_set.add(collection["collection"])
                        self.component_category_entity_list.append({"component_category_name": collection["collection"]})
                    if collection["area"] not in tmp_component_category_entity_set:
                        tmp_component_category_entity_set.add(collection["area"])
                        self.component_category_entity_list.append({"component_category_name": collection["area"]})
                    self.relation_list.append(
                        {"end_name": collection["collection"], "relation_type": 16, "start_name": item["full_name"]})
                    self.relation_list.append(
                        {"end_name": collection["collection"], "relation_type": 3, "start_name": collection["area"]})
        print("end generate component related entity and relation")

    def generate_evaluation_related_entity_relation(self):
        print("start generate evaluation related entity and relation")
        with gzip.open(str(Path(DATA_DIR) / "evaluation-tables.json.gz"), 'rt', encoding='UTF-8') as f:
            json_list = json.load(f)
        for item in json_list:
            self.recursion_task_in_evaluation([item])
        print("end generate evaluation related entity and relation")

    def recursion_task_in_evaluation(self, task_dict_list):
        for task_dict in task_dict_list:
            self.recursion_task_in_evaluation(task_dict["subtasks"])

            def recursion_dataset_in_evaluation(datasets):
                for dataset in datasets:
                    recursion_dataset_in_evaluation(dataset["subdatasets"])
                    for index, row in enumerate(dataset["sota"]["rows"]):
                        self.evaluation_entity_list.append({
                            "evaluation_name": str(row["metrics"]),
                            "rank": index + 1,
                        })
                        if row["model_name"] != "":
                            if row["model_name"] not in self.model_name_set:
                                self.model_name_set.add(row["model_name"])
                                self.model_entity_list.append({
                                    "model_name": row["model_name"],
                                    "alias": "",
                                    "extraction_source": 1,
                                    "model_speed": ""
                                })
                            self.relation_list.append(
                                {"end_name": str(row["metrics"]), "relation_type": 12, "start_name": row["model_name"]})
                            self.relation_list.append(
                                {"end_name": task_dict["task"], "relation_type": 2, "start_name": row["model_name"]})
                            if row["paper_title"] != "":
                                if row["paper_title"].lower() not in self.title2id:
                                    self.title2id[row["paper_title"].lower()] = self.MAX_PAPER_ID
                                    self.paper_entity_list.append({
                                        "paper_id": self.MAX_PAPER_ID,
                                        "title": row["paper_title"],
                                        "author": "",
                                        "abstract": "",
                                        "keyword": "",
                                        "conference": "",
                                        "year": int(row["paper_date"].split('-')[0]),
                                        "paper_url": row["paper_url"],
                                        "pdf_url": ""
                                    })
                                    self.MAX_PAPER_ID += 1
                                self.relation_list.append(
                                    {"end_name": self.title2id[row["paper_title"].lower()], "relation_type": 1,
                                     "start_name": row["model_name"]})

                        self.relation_list.append(
                            {"end_name": task_dict["task"], "relation_type": 13, "start_name": str(row["metrics"])})
                        self.relation_list.append(
                            {"end_name": dataset["dataset"], "relation_type": 14, "start_name": str(row["metrics"])})
                        self.relation_list.append(
                            {"end_name": dataset["dataset"], "relation_type": 15, "start_name": task_dict["task"]})

            recursion_dataset_in_evaluation(task_dict["datasets"])

    @staticmethod
    def Upper_first_letter(string: str):
        new_w_list = []
        w_list = string.split(' ')
        for w in w_list:
            if w == '':
                continue
            new_w_list.append(w[0].upper() + w[1:])
        return ' '.join(new_w_list)


if __name__ == '__main__':
    generator = EntityRelationGenerator()
    generator.generate_entity_relation()
