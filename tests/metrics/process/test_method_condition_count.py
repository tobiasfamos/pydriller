import pytest

from pydriller.metrics.process.method_condition_count import MethodConditionCount

TEST_DATA = [
    (
        'test-repos/method-test5', None, None,
        "Foo.java:Foo::noConditionInMethod()", {
            "condition_changes": 0,
            "else_added": 0,
            "else_removed": 0
        }),
    ('test-repos/method-test5', None, None, "Foo.java:Foo::neverAConditionChange()",
     {
         "condition_changes": 1,
         "else_added": 0,
         "else_removed": 0
     }),
    (
        'test-repos/method-test5', None, None,
        "Foo.java:Foo::conditionChangedOnce()",
        {
            "condition_changes": 3,
            "else_added": 0,
            "else_removed": 0
        }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::conditionChangedTwice()", {
         "condition_changes": 5,
         "else_added": 0,
         "else_removed": 0
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::twoDifferentConditionStatementsAdded()", {
         "condition_changes": 2,
         "else_added": 0,
         "else_removed": 0
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::oneConditionAddedAndRemovedAfter()", {
         "condition_changes": 2,
         "else_added": 1,
         "else_removed": 1
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::oneElseNeverChanged()", {
         "condition_changes": 1,
         "else_added": 1,
         "else_removed": 0
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::oneDeletedAfter()", {
         "condition_changes": 1,
         "else_added": 1,
         "else_removed": 1
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::twoElseOneDeleted()", {
         "condition_changes": 2,
         "else_added": 2,
         "else_removed": 1
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::fourElseAddedNoDeleted()", {
         "condition_changes": 4,
         "else_added": 4,
         "else_removed": 0
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::fourElseAddedAndDeleted()", {
         "condition_changes": 7,
         "else_added": 4,
         "else_removed": 4
     }),
    ('test-repos/method-test5', None, None,
     "Foo.java:Foo::twoElseIfAddedOneDeleted( int a)", {
         "condition_changes": 4,
         "else_added": 2,
         "else_removed": 1
     }),
]


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, function_name, expected', TEST_DATA)
def test_simple(path_to_repo, from_commit, to_commit, function_name, expected):
    metric = MethodConditionCount(path_to_repo=path_to_repo,
                               from_commit=from_commit,
                               to_commit=to_commit)

    method_count = metric.count()
    assert method_count[function_name] == expected
