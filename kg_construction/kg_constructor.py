#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC
from pathlib import Path
from sekg.pipeline.component.base import Component
from sekg.graph.exporter.graph_data import GraphData
from data_util import DataUtil
from definitions import OUTPUT_DIR
from project.kg_construction.entity_relation_category import RelationCategory, EntityCategory


class AIImporterComponent(Component, ABC):
    def __init__(self, graph_data=None, doc_collection=None):
        super().__init__(graph_data, doc_collection)

    def run(self, relation_path, paper_entity_path, task_entity_path, model_entity_path, repository_entity_path,
            license_entity_path, framework_entity_path, third_party_library_entity_path,
            language_version_entity_path, dataset_entity_path, hardware_entity_path, operation_system_entity_path,
            component_entity_path, component_category_entity_path, evaluation_entity_path,
            model_implementation_entity_path, computing_platform_entity_path):
        print("running component %r" % (self.type()))
        paper_name_to_node_id_map = self.import_entity_from_paper_list(paper_entity_path)
        task_name_to_node_id_map = self.import_entity_from_task_list(task_entity_path)
        model_name_to_node_id_map = self.import_entity_from_model_list(model_entity_path)
        repository_name_to_node_id_map = self.import_entity_from_repository_list(repository_entity_path)
        license_name_to_node_id_map = self.import_entity_from_license_list(license_entity_path)
        language_version_name_to_node_id_map = self.import_entity_from_language_version_list(language_version_entity_path)
        framework_name_to_node_id_map = self.import_entity_from_framework_list(framework_entity_path)
        third_party_library_name_to_node_id_map = self.import_entity_from_third_party_library_entity_list(third_party_library_entity_path)
        dataset_name_to_node_id_map = self.import_entity_from_dataset_entity_list(dataset_entity_path)
        hardware_name_to_node_id_map = self.import_entity_from_hardware_entity_list(hardware_entity_path)
        operation_system_name_to_node_id_map = self.import_entity_from_operation_system_entity_list(operation_system_entity_path)
        component_name_to_node_id_map = self.import_entity_from_component_entity_list(component_entity_path)
        component_category_name_to_node_id_map = self.import_entity_from_component_category_entity_list(component_category_entity_path)
        evaluation_name_to_node_id_map = self.import_entity_from_evaluation_entity_list(evaluation_entity_path)
        model_implementation_name_to_node_id_map = self.import_entity_from_model_implementation_entity_list(model_implementation_entity_path)
        computing_platform_name_to_node_id_map = self.import_entity_from_computing_platform_entity_list(computing_platform_entity_path)
        relations = self.insert_relations(relation_path=relation_path,
                                          paper_name_to_node_id_map=paper_name_to_node_id_map,
                                          task_name_to_node_id_map=task_name_to_node_id_map,
                                          model_name_to_node_id_map=model_name_to_node_id_map,
                                          repository_name_to_node_id_map=repository_name_to_node_id_map,
                                          license_name_to_node_id_map=license_name_to_node_id_map,
                                          language_version_name_to_node_id_map=language_version_name_to_node_id_map,
                                          framework_name_to_node_id_map=framework_name_to_node_id_map,
                                          third_party_library_name_to_node_id_map=third_party_library_name_to_node_id_map,
                                          dataset_name_to_node_id_map=dataset_name_to_node_id_map,
                                          hardware_name_to_node_id_map=hardware_name_to_node_id_map,
                                          operation_system_name_to_node_id_map=operation_system_name_to_node_id_map,
                                          component_name_to_node_id_map=component_name_to_node_id_map,
                                          component_category_name_to_node_id_map=component_category_name_to_node_id_map,
                                          evaluation_name_to_node_id_map=evaluation_name_to_node_id_map,
                                          model_implementation_name_to_node_id_map=model_implementation_name_to_node_id_map,
                                          computing_platform_name_to_node_id_map=computing_platform_name_to_node_id_map)
        self.import_relation_from_list(relations)
        print("end build graph")

    def import_normal_entity(self, entity_json, label_list, primary_property_name):
        node_id = self.graph_data.add_node(node_id=GraphData.UNASSIGNED_NODE_ID,
                                           node_labels=label_list,
                                           node_properties=entity_json,
                                           primary_property_name=primary_property_name)
        return node_id

    def import_entity_from_paper_list(self, paper_entity_path):
        print("start import paper node from list")
        entity_name_to_node_id_map = {}
        paper_entity_list = DataUtil.load_json_array(paper_entity_path)
        for entity_info_row in paper_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_PAPER})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "paper"],
                                                primary_property_name="paper_id")
            entity_name_to_node_id_map[entity_info_row["paper_id"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from paper list")
        return entity_name_to_node_id_map

    def import_entity_from_task_list(self, task_entity_path):
        print("start import task node from list")
        entity_name_to_node_id_map = {}
        task_entity_list = DataUtil.load_json_array(task_entity_path)
        for entity_info_row in task_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_TASK})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "task"],
                                                primary_property_name="task")
            entity_name_to_node_id_map[entity_info_row["task"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from task list")
        return entity_name_to_node_id_map

    def import_entity_from_model_list(self, model_entity_path):
        print("start import model node from list")
        entity_name_to_node_id_map = {}
        model_entity_list = DataUtil.load_json_array(model_entity_path)
        for entity_info_row in model_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_MODEL})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "model"],
                                                primary_property_name="model_name")
            entity_name_to_node_id_map[entity_info_row["model_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from model list")
        return entity_name_to_node_id_map

    def import_entity_from_repository_list(self, repository_entity_path):
        print("start import repository node from list")
        entity_name_to_node_id_map = {}
        repository_entity_list = DataUtil.load_json_array(repository_entity_path)
        for entity_info_row in repository_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_Repository})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "repository"],
                                                primary_property_name="implementation_id")
            entity_name_to_node_id_map[entity_info_row["implementation_id"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from repository list")
        return entity_name_to_node_id_map

    def import_entity_from_license_list(self, license_entity_path):
        print("start import license node from list")
        entity_name_to_node_id_map = {}
        license_entity_list = DataUtil.load_json_array(license_entity_path)
        for entity_info_row in license_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_LICENSE})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "license"],
                                                primary_property_name="license_name")
            entity_name_to_node_id_map[entity_info_row["license_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from license list")
        return entity_name_to_node_id_map

    def import_entity_from_language_version_list(self, language_version_entity_path):
        print("start import language version node from list")
        entity_name_to_node_id_map = {}
        language_version_entity_list = DataUtil.load_json_array(language_version_entity_path)
        for entity_info_row in language_version_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_PROGRAMMING_LANGUAGE})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "programming language"],
                                                primary_property_name="language_version_name")
            entity_name_to_node_id_map[entity_info_row["language_version_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from language version list")
        return entity_name_to_node_id_map

    def import_entity_from_framework_list(self, framework_entity_path):
        print("start import framework node from list")
        entity_name_to_node_id_map = {}
        framework_entity_list = DataUtil.load_json_array(framework_entity_path)
        for entity_info_row in framework_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_AI_FRAMEWORK})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "framework"],
                                                primary_property_name="framework_name")
            entity_name_to_node_id_map[entity_info_row["framework_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from framework list")
        return entity_name_to_node_id_map

    def import_entity_from_third_party_library_entity_list(self, third_party_library_entity_path):
        print("start import third party library node from list")
        entity_name_to_node_id_map = {}
        third_party_library_entity_list = DataUtil.load_json_array(third_party_library_entity_path)
        for entity_info_row in third_party_library_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_THIRD_PARTY_LIBRARY})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "third party library"],
                                                primary_property_name="library_name")
            entity_name_to_node_id_map[entity_info_row["library_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from third party library list")
        return entity_name_to_node_id_map

    def import_entity_from_dataset_entity_list(self, dataset_entity_path):
        print("start import dataset node from list")
        entity_name_to_node_id_map = {}
        dataset_entity_list = DataUtil.load_json_array(dataset_entity_path)
        for entity_info_row in dataset_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_DATASET})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "dataset"],
                                                primary_property_name="dataset_name")
            entity_name_to_node_id_map[entity_info_row["dataset_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from dataset list")
        return entity_name_to_node_id_map

    def import_entity_from_hardware_entity_list(self, hardware_entity_path):
        print("start import hardware node from list")
        entity_name_to_node_id_map = {}
        hardware_entity_list = DataUtil.load_json_array(hardware_entity_path)
        for entity_info_row in hardware_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_HARDWARE})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "hardware"],
                                                primary_property_name="hardware_name")
            entity_name_to_node_id_map[entity_info_row["hardware_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from hardware list")
        return entity_name_to_node_id_map

    def import_entity_from_operation_system_entity_list(self, operation_system_entity_path):
        print("start import operation system node from list")
        entity_name_to_node_id_map = {}
        operation_system_entity_list = DataUtil.load_json_array(operation_system_entity_path)
        for entity_info_row in operation_system_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_OPERATION_SYSTEM})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "operation system"],
                                                primary_property_name="operation_system_name")
            entity_name_to_node_id_map[entity_info_row["operation_system_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from operation system list")
        return entity_name_to_node_id_map

    def import_entity_from_component_entity_list(self, component_entity_path):
        print("start import component node from list")
        entity_name_to_node_id_map = {}
        component_entity_list = DataUtil.load_json_array(component_entity_path)
        for entity_info_row in component_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_COMPONENT})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "component"],
                                                primary_property_name="component_name")
            entity_name_to_node_id_map[entity_info_row["component_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from component list")
        return entity_name_to_node_id_map

    def import_entity_from_component_category_entity_list(self, component_category_entity_path):
        print("start import component category node from list")
        entity_name_to_node_id_map = {}
        component_category_entity_list = DataUtil.load_json_array(component_category_entity_path)
        for entity_info_row in component_category_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_COMPONENT_CATEGORY})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "component category"],
                                                primary_property_name="component_category_name")
            entity_name_to_node_id_map[entity_info_row["component_category_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from component category list")
        return entity_name_to_node_id_map

    def import_entity_from_evaluation_entity_list(self, evaluation_entity_path):
        print("start import evaluation node from list")
        entity_name_to_node_id_map = {}
        evaluation_entity_list = DataUtil.load_json_array(evaluation_entity_path)
        for entity_info_row in evaluation_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_EVALUATION})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "evaluation"],
                                                primary_property_name="evaluation_name")
            entity_name_to_node_id_map[entity_info_row["evaluation_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from evaluation list")
        return entity_name_to_node_id_map

    def import_entity_from_model_implementation_entity_list(self, model_implementation_entity_path):
        print("start import model implementation node from list")
        entity_name_to_node_id_map = {}
        model_implementation_entity_list = DataUtil.load_json_array(model_implementation_entity_path)
        for entity_info_row in model_implementation_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_MODEL_IMPLEMENTATION})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "model implementation"],
                                                primary_property_name="model_implementation_name")
            entity_name_to_node_id_map[entity_info_row["model_implementation_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from model implementation list")
        return entity_name_to_node_id_map

    def import_entity_from_computing_platform_entity_list(self, computing_platform_entity_path):
        print("start import computing platform node from list")
        entity_name_to_node_id_map = {}
        computing_platform_entity_list = DataUtil.load_json_array(computing_platform_entity_path)
        for entity_info_row in computing_platform_entity_list:
            entity_info_row.update({"node_id": self.graph_data.max_node_id,
                                    "entity_type": EntityCategory.CATEGORY_COMPUTING_PLATFORM})
            node_id = self.import_normal_entity(entity_json=entity_info_row,
                                                label_list=["entity", "computing platform"],
                                                primary_property_name="computing_platform_name")
            entity_name_to_node_id_map[entity_info_row["computing_platform_name"]] = node_id
        self.graph_data.print_graph_info()
        print("end import from computing platform list")
        return entity_name_to_node_id_map

    def insert_relations(self, relation_path, paper_name_to_node_id_map, task_name_to_node_id_map,
                         model_name_to_node_id_map, repository_name_to_node_id_map, license_name_to_node_id_map,
                         language_version_name_to_node_id_map, framework_name_to_node_id_map,
                         third_party_library_name_to_node_id_map, dataset_name_to_node_id_map,
                         hardware_name_to_node_id_map, operation_system_name_to_node_id_map,
                         component_name_to_node_id_map, component_category_name_to_node_id_map,
                         evaluation_name_to_node_id_map, model_implementation_name_to_node_id_map,
                         computing_platform_name_to_node_id_map):
        relations = []
        relation_list = DataUtil.load_json_array(relation_path)
        for r in relation_list:
            if r["relation_type"] == 1:
                if r["start_name"] in model_name_to_node_id_map.keys() and \
                        r["end_name"] in paper_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_PROPOSED_IN
                    start_id = model_name_to_node_id_map[r["start_name"]]
                    end_id = paper_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 2:
                if r["start_name"] in model_name_to_node_id_map.keys() and \
                        r["end_name"] in task_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_ACCOMPLISH
                    start_id = model_name_to_node_id_map[r["start_name"]]
                    end_id = task_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 3:
                if r["start_name"] in task_name_to_node_id_map.keys() and \
                        r["end_name"] in task_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUBCLASS_OF
                    start_id = task_name_to_node_id_map[r["start_name"]]
                    end_id = task_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in component_category_name_to_node_id_map.keys() and \
                        r["end_name"] in component_category_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUBCLASS_OF
                    start_id = component_category_name_to_node_id_map[r["start_name"]]
                    end_id = component_category_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in operation_system_name_to_node_id_map.keys() and \
                        r["end_name"] in operation_system_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUBCLASS_OF
                    start_id = operation_system_name_to_node_id_map[r["start_name"]]
                    end_id = operation_system_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 4:
                if r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in model_implementation_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_PROVIDE
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = model_implementation_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 5:
                if r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in framework_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_BASE_ON
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = framework_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in framework_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_BASE_ON
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = framework_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 6:
                if r["start_name"] in computing_platform_name_to_node_id_map.keys() and \
                        r["end_name"] in hardware_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_RUN_ON
                    start_id = computing_platform_name_to_node_id_map[r["start_name"]]
                    end_id = hardware_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 7:
                if r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in operation_system_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUPPORT
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = operation_system_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in operation_system_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUPPORT
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = operation_system_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in hardware_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUPPORT
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = hardware_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in hardware_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUPPORT
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = hardware_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in language_version_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUPPORT
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = language_version_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in language_version_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_SUPPORT
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = language_version_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 8:
                if r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in dataset_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_USE
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = dataset_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in dataset_name_to_node_id_map:
                    relation_type = RelationCategory.RELATION_USE
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = dataset_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in model_name_to_node_id_map.keys() and \
                        r["end_name"] in component_name_to_node_id_map:
                    relation_type = RelationCategory.RELATION_USE
                    start_id = model_name_to_node_id_map[r["start_name"]]
                    end_id = component_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 9:
                if r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in third_party_library_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_DEPEND_ON
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = third_party_library_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in third_party_library_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_DEPEND_ON
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = third_party_library_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 10:
                if r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in license_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_LICENSE
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = license_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 11:
                if r["start_name"] in framework_name_to_node_id_map.keys() and \
                        r["end_name"] in component_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_IMPLEMENT
                    start_id = framework_name_to_node_id_map[r["start_name"]]
                    end_id = component_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in model_implementation_name_to_node_id_map.keys() and \
                        r["end_name"] in model_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_IMPLEMENT
                    start_id = model_implementation_name_to_node_id_map[r["start_name"]]
                    end_id = model_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 12:
                if r["start_name"] in model_name_to_node_id_map.keys() and \
                        r["end_name"] in evaluation_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_EVALUATION
                    start_id = model_name_to_node_id_map[r["start_name"]]
                    end_id = evaluation_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 13:
                if r["start_name"] in evaluation_name_to_node_id_map.keys() and \
                        r["end_name"] in task_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_PERFORMED_FOR
                    start_id = evaluation_name_to_node_id_map[r["start_name"]]
                    end_id = task_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 14:
                if r["start_name"] in evaluation_name_to_node_id_map.keys() and \
                        r["end_name"] in dataset_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_PERFORMED_ON
                    start_id = evaluation_name_to_node_id_map[r["start_name"]]
                    end_id = dataset_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 15:
                if r["start_name"] in task_name_to_node_id_map.keys() and \
                        r["end_name"] in dataset_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_DATASET
                    start_id = task_name_to_node_id_map[r["start_name"]]
                    end_id = dataset_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 16:
                if r["start_name"] in component_name_to_node_id_map.keys() and \
                        r["end_name"] in component_category_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_BELONG_TO
                    start_id = component_name_to_node_id_map[r["start_name"]]
                    end_id = component_category_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 17:
                if r["start_name"] in repository_name_to_node_id_map.keys() and \
                        r["end_name"] in task_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_ASSOCIATE
                    start_id = repository_name_to_node_id_map[r["start_name"]]
                    end_id = task_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in model_name_to_node_id_map.keys() and \
                        r["end_name"] in paper_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_ASSOCIATE
                    start_id = model_name_to_node_id_map[r["start_name"]]
                    end_id = paper_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 18:
                if r["start_name"] in framework_name_to_node_id_map.keys() and \
                        r["end_name"] in framework_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_VERSION
                    start_id = framework_name_to_node_id_map[r["start_name"]]
                    end_id = framework_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in language_version_name_to_node_id_map.keys() and \
                        r["end_name"] in language_version_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_VERSION
                    start_id = language_version_name_to_node_id_map[r["start_name"]]
                    end_id = language_version_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in computing_platform_name_to_node_id_map.keys() and \
                        r["end_name"] in computing_platform_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_VERSION
                    start_id = computing_platform_name_to_node_id_map[r["start_name"]]
                    end_id = computing_platform_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in third_party_library_name_to_node_id_map.keys() and \
                        r["end_name"] in third_party_library_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_HAS_VERSION
                    start_id = third_party_library_name_to_node_id_map[r["start_name"]]
                    end_id = third_party_library_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
            elif r["relation_type"] == 19:
                if r["start_name"] in framework_name_to_node_id_map.keys() and \
                        r["end_name"] in framework_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_INSTANCE_OF
                    start_id = framework_name_to_node_id_map[r["start_name"]]
                    end_id = framework_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in hardware_name_to_node_id_map.keys() and \
                        r["end_name"] in hardware_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_INSTANCE_OF
                    start_id = hardware_name_to_node_id_map[r["start_name"]]
                    end_id = hardware_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in language_version_name_to_node_id_map.keys() and \
                        r["end_name"] in language_version_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_INSTANCE_OF
                    start_id = language_version_name_to_node_id_map[r["start_name"]]
                    end_id = language_version_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in computing_platform_name_to_node_id_map.keys() and \
                        r["end_name"] in computing_platform_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_INSTANCE_OF
                    start_id = computing_platform_name_to_node_id_map[r["start_name"]]
                    end_id = computing_platform_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                elif r["start_name"] in operation_system_name_to_node_id_map.keys() and \
                        r["end_name"] in operation_system_name_to_node_id_map.keys():
                    relation_type = RelationCategory.RELATION_INSTANCE_OF
                    start_id = operation_system_name_to_node_id_map[r["start_name"]]
                    end_id = operation_system_name_to_node_id_map[r["end_name"]]
                    relations.append([start_id, end_id, relation_type])
                else:
                    print(r)
                    continue
        return relations

    def import_relation_from_list(self, relations):
        print("start import relation")
        self.graph_data.print_graph_info()
        for row in relations:
            if len(row) == 3:
                self.graph_data.add_relation(startId=row[0],
                                             endId=row[1],
                                             relationType=RelationCategory.to_str(row[2]))
            else:
                self.graph_data.add_relation_with_property(startId=row[0],
                                                           endId=row[1],
                                                           relationType=RelationCategory.to_str(row[2]),
                                                           version=row[3]["version"])
        print("end import relation")
        self.graph_data.print_graph_info()

    def save(self, g_path):
        self.graph_data.save(g_path)


if __name__ == '__main__':
    relation_path = str(Path(OUTPUT_DIR) / "entity_relation_data/relation.json")
    paper_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/paper_entity.json")
    task_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/task_entity.json")
    model_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/model_entity.json")
    repository_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/repository_entity.json")
    license_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/license_entity.json")
    framework_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/framework_entity.json")
    third_party_library_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/third_party_library_entity.json")
    language_version_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/language_version_entity.json")
    dataset_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/dataset_entity.json")
    hardware_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/hardware_entity.json")
    operation_system_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/operation_system_entity.json")
    component_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/component_entity.json")
    component_category_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/component_category_entity.json")
    evaluation_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/evaluation_entity.json")
    model_implementation_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/model_implementation_entity.json")
    computing_platform_entity_path = str(Path(OUTPUT_DIR) / "entity_relation_data/computing_platform_entity.json")
    graph_save_path = str(Path(OUTPUT_DIR) / "graph/AIKG_v8.graph")
    component = AIImporterComponent()
    component.run(relation_path=relation_path,
                  paper_entity_path=paper_entity_path,
                  task_entity_path=task_entity_path,
                  model_entity_path=model_entity_path,
                  repository_entity_path=repository_entity_path,
                  license_entity_path=license_entity_path,
                  framework_entity_path=framework_entity_path,
                  third_party_library_entity_path=third_party_library_entity_path,
                  language_version_entity_path=language_version_entity_path,
                  dataset_entity_path=dataset_entity_path,
                  hardware_entity_path=hardware_entity_path,
                  operation_system_entity_path=operation_system_entity_path,
                  component_entity_path=component_entity_path,
                  component_category_entity_path=component_category_entity_path,
                  evaluation_entity_path=evaluation_entity_path,
                  model_implementation_entity_path=model_implementation_entity_path,
                  computing_platform_entity_path=computing_platform_entity_path)
    component.save(graph_save_path)
