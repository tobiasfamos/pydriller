import pytest

from pathlib import Path
from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.method_statement_count import MethodStatementCount

TEST_DATA = [
    ('test-repos/method-test', None, 'c155c3ee786f40dca1f4e9c59ab989d0b252df80', "Foo.java:Foo::someFunction()",
     {"sum_statement_added": 6}),
    ('test-repos/method-test', None, 'c155c3ee786f40dca1f4e9c59ab989d0b252df80', "Foo.java:Foo::someFunction2()",
     {"sum_statement_added": 6}),
    ('test-repos/method-test', None, 'c155c3ee786f40dca1f4e9c59ab989d0b252df80', "Foo.java:Foo::someFunction3()",
     {"sum_statement_added": 6}),
    ('test-repos/method-test', None, None, "Bar.java:Foo::someFunction()",
     {"sum_statement_added": 4}),
    ('test-repos/method-test', None, None, "Bar.java:Foo::someFunction2()",
     {"sum_statement_added": 4}),
    ('test-repos/method-test', None, None, "Bar.java:Foo::someFunction3()",
     {"sum_statement_added": 4})
]


@pytest.mark.parametrize('path_to_repo, from_commit, to_commit, function_name, expected', TEST_DATA)
def test(path_to_repo, from_commit, to_commit, function_name, expected):
    metric = MethodStatementCount(path_to_repo=path_to_repo,
                                  from_commit=from_commit,
                                  to_commit=to_commit)

    method_count = metric.count()
    assert method_count[function_name] == expected
