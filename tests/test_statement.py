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


def test_method_stmt_added(resource):
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
