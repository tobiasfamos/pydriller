import pytest

from pydriller.metrics.process.method_declaration_count import MethodDeclarationCount

TEST_DATA = [
    (
        'test-repos/method-test4', None, None,
        "Foo.java:Foo::methodDeclarationNeverChanged()", 1),
    ('test-repos/method-test4', None, None, "Foo.java:Foo::methodNameChangedOnce1()",
     2),
    (
        'test-repos/method-test4', None, None,
        "Foo.java:Foo::methodNameAndRetrurnTypeChangeOnceTogether1()",
        2),
    ('test-repos/method-test4', None, None,
     "Foo.java:Foo::methodNameAndRetrurnTypeChangeOnceSeperate1()", 3),
    ('test-repos/method-test4', None, None,
     "Foo.java:Foo::methodVisibilityChangedOnce()", 2),
    ('test-repos/method-test4', None, None,
     "Foo.java:Foo::methodChangedThreeTimes3()", 4)
]


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, function_name, expected', TEST_DATA)
def test_simple(path_to_repo, from_commit, to_commit, function_name, expected):
    metric = MethodDeclarationCount(path_to_repo=path_to_repo,
                                    from_commit=from_commit,
                                    to_commit=to_commit)

    method_count = metric.count()
    assert method_count[function_name] == expected

