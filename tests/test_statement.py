# Copyright 2018 Davide Spadini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest
from pydriller.git_repository import GitRepository


@pytest.yield_fixture(scope="module")
def resource():
    yield GitRepository('test-repos/git-1/')


def test_method_exec_statements(resource):
    modifications_c1 = resource.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559').modifications
    modifications_c2 = resource.get_commit('8b1757781e2e05c22fad91566e4f2653453dc934').modifications

    assert modifications_c1[0].methods[0].exec_statements == 0
    assert modifications_c1[0].methods[1].exec_statements == 4
    assert modifications_c1[0].methods[2].exec_statements == 1
    assert modifications_c1[0].methods[3].exec_statements == 1
    assert modifications_c1[0].methods[4].exec_statements == 1
    assert modifications_c1[0].methods[5].exec_statements == 1
    assert modifications_c1[0].methods[6].exec_statements == 1

    assert modifications_c2[0].methods[0].exec_statements == 0
    assert modifications_c2[0].methods[1].exec_statements == 2
    assert modifications_c2[0].methods[2].exec_statements == 1
    assert modifications_c2[0].methods[3].exec_statements == 1
    assert modifications_c2[0].methods[4].exec_statements == 1
    assert modifications_c2[0].methods[5].exec_statements == 2


def test_method_statements_added_new_file(resource):
    modifications_c1 = resource.get_commit('866e997a9e44cb4ddd9e00efe49361420aff2559').modifications
    modifications_c2 = resource.get_commit('8b1757781e2e05c22fad91566e4f2653453dc934').modifications

    assert modifications_c1[0].methods[0].statements_added == 0
    assert modifications_c1[0].methods[1].statements_added == 4
    assert modifications_c1[0].methods[2].statements_added == 1
    assert modifications_c1[0].methods[3].statements_added == 1
    assert modifications_c1[0].methods[4].statements_added == 1
    assert modifications_c1[0].methods[5].statements_added == 1
    assert modifications_c1[0].methods[6].statements_added == 1

    assert modifications_c2[0].methods[0].statements_added == 0
    assert modifications_c2[0].methods[1].statements_added == 2
    assert modifications_c2[0].methods[2].statements_added == 1
    assert modifications_c2[0].methods[3].statements_added == 1
    assert modifications_c2[0].methods[4].statements_added == 1
    assert modifications_c2[0].methods[5].statements_added == 2


def test_method_statements_added_exiting_file(resource):
    modifications_c3 = resource.get_commit('57dbd017d1a744b949e7ca0b1c1a3b3dd4c1cbc1').modifications

    assert modifications_c3[0].methods[0].statements_added == 0
    assert modifications_c3[0].methods[1].statements_added == 0
    assert modifications_c3[0].methods[2].statements_added == 1
    assert modifications_c3[0].methods[3].statements_added == 0
    assert modifications_c3[0].methods[4].statements_added == 0
    assert modifications_c3[0].methods[5].statements_added == 0
    assert modifications_c3[0].methods[6].statements_added == 0

def test_method_statements_deleted_existing_file(resource):
    modifications = resource.get_commit('e7d13b0511f8a176284ce4f92ed8c6e8d09c77f2').modifications

    assert modifications[0].methods[0].statements_deleted == 1

def test_statement_overall():
    git = GitRepository('test-repos/method-test/')
    creation_modifcations = git.get_commit('6473c2c63ce09cda65bb11cf1f1bf12f31c185a2').modifications
    assert creation_modifcations[0].methods[0].exec_statements == 3
    assert creation_modifcations[0].methods[0].statements_added == 3
    assert creation_modifcations[0].methods[0].statements_deleted == 0

    assert creation_modifcations[0].methods[1].exec_statements == 3
    assert creation_modifcations[0].methods[1].statements_added == 3
    assert creation_modifcations[0].methods[1].statements_deleted == 0

    assert creation_modifcations[0].methods[2].exec_statements == 3
    assert creation_modifcations[0].methods[2].statements_added == 3
    assert creation_modifcations[0].methods[2].statements_deleted == 0

    one_statement_deleted_modification = git.get_commit('6b589757f66986981d1ef367304ae7f4371acd27').modifications
    assert one_statement_deleted_modification[0].methods[0].exec_statements == 2
    assert one_statement_deleted_modification[0].methods[0].statements_added == 0
    assert one_statement_deleted_modification[0].methods[0].statements_deleted == 1

    assert one_statement_deleted_modification[0].methods[1].exec_statements == 2
    assert one_statement_deleted_modification[0].methods[1].statements_added == 0
    assert one_statement_deleted_modification[0].methods[1].statements_deleted == 1

    assert one_statement_deleted_modification[0].methods[2].exec_statements == 2
    assert one_statement_deleted_modification[0].methods[2].statements_added == 0
    assert one_statement_deleted_modification[0].methods[2].statements_deleted == 1

    one_statement_added_modification = git.get_commit('2e533a7e1a0672ffd9f5c3b18dfadd4e34702bd1').modifications
    assert one_statement_added_modification[0].methods[0].exec_statements == 3
    assert one_statement_added_modification[0].methods[0].statements_added == 1
    assert one_statement_added_modification[0].methods[0].statements_deleted == 0

    assert one_statement_added_modification[0].methods[1].exec_statements == 3
    assert one_statement_added_modification[0].methods[1].statements_added == 1
    assert one_statement_added_modification[0].methods[1].statements_deleted == 0

    assert one_statement_added_modification[0].methods[2].exec_statements == 3
    assert one_statement_added_modification[0].methods[2].statements_added == 1
    assert one_statement_added_modification[0].methods[2].statements_deleted == 0

    one_added_one_deleted_modification = git.get_commit('af64155895273010b8e6cc793083a088c5fa45cb').modifications
    assert one_added_one_deleted_modification[0].methods[0].exec_statements == 3
    assert one_added_one_deleted_modification[0].methods[0].statements_added == 1
    assert one_added_one_deleted_modification[0].methods[0].statements_deleted == 1

    assert one_added_one_deleted_modification[0].methods[1].exec_statements == 3
    assert one_added_one_deleted_modification[0].methods[1].statements_added == 1
    assert one_added_one_deleted_modification[0].methods[1].statements_deleted == 1

    assert one_added_one_deleted_modification[0].methods[2].exec_statements == 3
    assert one_added_one_deleted_modification[0].methods[2].statements_added == 1
    assert one_added_one_deleted_modification[0].methods[2].statements_deleted == 1

    no_statement_added_modification = git.get_commit('fcd8f8eae9c6d249621271d14376dabdedf843bb').modifications
    assert no_statement_added_modification[0].methods[0].exec_statements == 3
    assert no_statement_added_modification[0].methods[0].statements_added == 0
    assert no_statement_added_modification[0].methods[0].statements_deleted == 0

    assert no_statement_added_modification[0].methods[1].exec_statements == 3
    assert no_statement_added_modification[0].methods[1].statements_added == 0
    assert no_statement_added_modification[0].methods[1].statements_deleted == 0

    assert no_statement_added_modification[0].methods[2].exec_statements == 3
    assert no_statement_added_modification[0].methods[2].statements_added == 0
    assert no_statement_added_modification[0].methods[2].statements_deleted == 0

    one_added_one_deleted_modification_2 = git.get_commit('c155c3ee786f40dca1f4e9c59ab989d0b252df80').modifications
    assert one_added_one_deleted_modification_2[0].methods[0].exec_statements == 3
    assert one_added_one_deleted_modification_2[0].methods[0].statements_added == 1
    assert one_added_one_deleted_modification_2[0].methods[0].statements_deleted == 1

    assert one_added_one_deleted_modification_2[0].methods[1].exec_statements == 3
    assert one_added_one_deleted_modification_2[0].methods[1].statements_added == 1
    assert one_added_one_deleted_modification_2[0].methods[1].statements_deleted == 1

    assert one_added_one_deleted_modification_2[0].methods[2].exec_statements == 3
    assert one_added_one_deleted_modification_2[0].methods[2].statements_added == 1
    assert one_added_one_deleted_modification_2[0].methods[2].statements_deleted == 1
