import pytest

from pydriller.metrics.process.method_author_count import MethodAuthorCount

TEST_DATA = [
    (
        'test-repos/method-test3', None, None,
        "Foo.java:Foo::methodOnlyChangedOne()", 1),
    ('test-repos/method-test3', None, None, "Foo.java:Foo::methodChangedByTwo()",
     2),
    (
        'test-repos/method-test3', None, None,
        "Foo.java:Foo::methodChangedByThree()",
        3),
    ('test-repos/method-test3', None, None,
     "Foo.java:Foo::methodChangedByTwoWithSameNameButDifferentEmail()", 2),
    ('test-repos/method-test3', None, None,
     "Foo.java:Foo::methodChangedBySameAuthorTwice()", 2),
    ('test-repos/method-test3', None, None,
     "Foo.java:Foo::methodChangedByTwoDifferentTwice()", 2)
]


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, function_name, expected', TEST_DATA)
def test_simple(path_to_repo, from_commit, to_commit, function_name, expected):
    metric = MethodAuthorCount(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)

    method_count = metric.count()
    assert method_count[function_name] == expected
