import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

import pytest
from pydriller.git_repository import GitRepository


@pytest.yield_fixture(scope="module")
def resource():
    yield GitRepository('test-repos/method-test6')


def test_comment_to_code_ratio(resource):
    modifications_c1 = resource.get_commit('1139c9ed62db5034a0b6e62a0d27350641bad949').modifications

    assert modifications_c1[0].methods[0].comment_to_code_ration == 1/3
    assert modifications_c1[0].methods[1].comment_to_code_ration == 1/4
    assert modifications_c1[0].methods[2].comment_to_code_ration == 3/2
    assert modifications_c1[0].methods[3].comment_to_code_ration == 4/3
    assert modifications_c1[0].methods[4].comment_to_code_ration == 3/3

