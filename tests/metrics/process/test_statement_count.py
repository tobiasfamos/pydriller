import pytest

from pathlib import Path
from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.method_statement_count import MethodStatementCount

EXPECTED_SIMPLE = {"sum_statement_added": 6,
                   "max_statement_added": 3,
                   "average_statement_added": 1.2,
                   "sum_statement_deleted": 3,
                   "max_statement_deleted": 1,
                   "average_statement_deleted": 0.6,
                   "method_histories": 5,
                   "churn": 3,
                   "max_churn": 3,
                   "average_churn": 0.6}

EXPECTED_RENAME = {"sum_statement_added": 4,
                   "max_statement_added": 3,
                   "average_statement_added": 1,
                   "sum_statement_deleted": 2,
                   "max_statement_deleted": 1,
                   "average_statement_deleted": 0.5,
                   "method_histories": 4,
                   "churn": 2,
                   "max_churn": 3,
                   "average_churn": 0.5}

TEST_DATA_SIMPLE = [
    ('test-repos/method-test', None, 'c155c3ee786f40dca1f4e9c59ab989d0b252df80', "Foo.java:Foo::someFunction()",
     EXPECTED_SIMPLE),
    ('test-repos/method-test', None, 'c155c3ee786f40dca1f4e9c59ab989d0b252df80', "Foo.java:Foo::someFunction2()",
     EXPECTED_SIMPLE),
    ('test-repos/method-test', None, 'c155c3ee786f40dca1f4e9c59ab989d0b252df80', "Foo.java:Foo::someFunction3()",
     EXPECTED_SIMPLE)]

TEST_DATA_RENAME = [
    ('test-repos/method-test2', None, "62339f6ae6cfea5b06c54dee1479b9d884afe260", "Bar.java:Foo::someFunction()",
     EXPECTED_RENAME
     ),
    ('test-repos/method-test2', None, "62339f6ae6cfea5b06c54dee1479b9d884afe260", "Bar.java:Foo::someFunction2()",
     EXPECTED_RENAME),
    ('test-repos/method-test2', None, "62339f6ae6cfea5b06c54dee1479b9d884afe260", "Bar.java:Foo::someFunction3()",
     EXPECTED_RENAME)
]


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, function_name, expected', TEST_DATA_SIMPLE)
def test_simple(path_to_repo, from_commit, to_commit, function_name, expected):
    metric = MethodStatementCount(path_to_repo=path_to_repo,
                                  from_commit=from_commit,
                                  to_commit=to_commit)

    method_count = metric.count()
    assert method_count[function_name] == expected


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, function_name, expected', TEST_DATA_RENAME)
def test_rename(path_to_repo, from_commit, to_commit, function_name, expected):
    metric = MethodStatementCount(path_to_repo=path_to_repo,
                                  from_commit=from_commit,
                                  to_commit=to_commit)

    method_count = metric.count()
    assert method_count[function_name] == expected
