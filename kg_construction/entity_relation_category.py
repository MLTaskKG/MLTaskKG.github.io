#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EntityCategory:
    CATEGORY_PAPER = 1
    CATEGORY_TASK = 2
    CATEGORY_MODEL = 3
    CATEGORY_Repository = 4
    CATEGORY_LICENSE = 5
    CATEGORY_PROGRAMMING_LANGUAGE = 6
    CATEGORY_AI_FRAMEWORK = 7
    CATEGORY_THIRD_PARTY_LIBRARY = 8
    CATEGORY_DATASET = 9
    CATEGORY_OPERATION_SYSTEM = 10
    CATEGORY_HARDWARE = 11
    CATEGORY_COMPONENT = 12
    CATEGORY_COMPONENT_CATEGORY = 13
    CATEGORY_EVALUATION = 14
    CATEGORY_MODEL_IMPLEMENTATION = 15
    CATEGORY_COMPUTING_PLATFORM = 16

    category_code_to_str_map = {
        CATEGORY_PAPER: "Paper",
        CATEGORY_TASK: "Task",
        CATEGORY_MODEL: "DL/ML Model",
        CATEGORY_Repository: "Repository",
        CATEGORY_LICENSE: "License",
        CATEGORY_PROGRAMMING_LANGUAGE: "Programming Language",
        CATEGORY_AI_FRAMEWORK: "AI Framework",
        CATEGORY_THIRD_PARTY_LIBRARY: "Third Party Library",
        CATEGORY_DATASET: "Dataset",
        CATEGORY_OPERATION_SYSTEM: "Operation System",
        CATEGORY_HARDWARE: "Hardware",
        CATEGORY_COMPONENT: "DL/ML Component",
        CATEGORY_COMPONENT_CATEGORY: "Component Category",
        CATEGORY_EVALUATION: "Evaluation",
        CATEGORY_MODEL_IMPLEMENTATION: "Model Implementation",
        CATEGORY_COMPUTING_PLATFORM: "Computing Platform"
    }

    @staticmethod
    def to_str(category_code):
        if category_code in EntityCategory.category_code_to_str_map:
            return EntityCategory.category_code_to_str_map[category_code]
        return "unknown"

    @staticmethod
    def entity_category_set():
        return EntityCategory.category_code_to_str_map.keys()


class RelationCategory:
    RELATION_PROPOSED_IN = 1
    RELATION_ACCOMPLISH = 2
    RELATION_SUBCLASS_OF = 3
    RELATION_PROVIDE = 4
    RELATION_BASE_ON = 5
    RELATION_RUN_ON = 6
    RELATION_SUPPORT = 7
    RELATION_USE = 8
    RELATION_DEPEND_ON = 9
    RELATION_HAS_LICENSE = 10
    RELATION_IMPLEMENT = 11
    RELATION_HAS_EVALUATION = 12
    RELATION_PERFORMED_FOR = 13
    RELATION_PERFORMED_ON = 14
    RELATION_HAS_DATASET = 15
    RELATION_BELONG_TO = 16
    RELATION_ASSOCIATE = 17
    RELATION_HAS_VERSION = 18
    RELATION_INSTANCE_OF = 19

    category_code_to_str_map = {
        RELATION_PROPOSED_IN: "proposed in",
        RELATION_ACCOMPLISH: "accomplish",
        RELATION_SUBCLASS_OF: "subclass of",
        RELATION_PROVIDE: "provide",
        RELATION_BASE_ON: "base on",
        RELATION_RUN_ON: "run on",
        RELATION_SUPPORT: "support",
        RELATION_USE: "use",
        RELATION_DEPEND_ON: "depend on",
        RELATION_HAS_LICENSE: "has license",
        RELATION_IMPLEMENT: "implement",
        RELATION_HAS_EVALUATION: "has evaluation",
        RELATION_PERFORMED_FOR: "performed for",
        RELATION_PERFORMED_ON: "performed on",
        RELATION_HAS_DATASET: "has dataset",
        RELATION_BELONG_TO: "belong to",
        RELATION_ASSOCIATE: "associate",
        RELATION_HAS_VERSION: "has version",
        RELATION_INSTANCE_OF: "instance of"
    }

    @staticmethod
    def to_str(category_code):
        if category_code in RelationCategory.category_code_to_str_map:
            return RelationCategory.category_code_to_str_map[category_code]
        return "unknown"

    @staticmethod
    def relation_category_set():
        return RelationCategory.category_code_to_str_map.keys()

    @staticmethod
    def str_to_category_code():
        str_to_code = {}
        for code in RelationCategory.category_code_to_str_map.keys():
            str_to_code[RelationCategory.category_code_to_str_map[code]] = code
        return str_to_code
