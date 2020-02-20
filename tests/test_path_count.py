import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest
from pydriller.git_repository import GitRepository


@pytest.yield_fixture(scope="module")
def resource():
    yield GitRepository('test-repos/method-test7')


def test_path_count(resource):
    modifications_c1 = resource.get_commit('3fc95bd06a2b5f74bc8169b3ae387b18daf2130f').modifications

    assert modifications_c1[0].methods[0].path_count == 0
    assert modifications_c1[0].methods[1].path_count == 1
    assert modifications_c1[0].methods[2].path_count == 1
    assert modifications_c1[0].methods[3].path_count == 2
    assert modifications_c1[0].methods[4].path_count == 5
    assert modifications_c1[0].methods[5].path_count == 1

def test_path_count_add_one(resource):
    modifications_c1 = resource.get_commit('40e6a53d400b168aebd5e15ead770ec5945ba564').modifications
    assert modifications_c1[0].methods[5].path_count == 2

def test_path_count_add_two(resource):
    modifications_c1 = resource.get_commit('3722266f043cd40c1bb5def0f33795971afcf035').modifications
    assert modifications_c1[0].methods[5].path_count == 3

