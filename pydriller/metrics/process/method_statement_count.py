"""
Module that calculates the number of commits made to a file.
"""

from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric


class MethodStatementCount(ProcessMetric):

    def count(self):
        methods = {}
        renamed_files = {}  # To keep track of renamed files

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:

                for method in modified_file.methods:
                    method_name = method.filename + ":" + method.long_name
                    previous_added = methods.get(method_name, {"sum_statement_added": 0})
                    previous_added["sum_statement_added"] = previous_added["sum_statement_added"] + method.statements_added
                    methods[method_name] = previous_added
        return methods
