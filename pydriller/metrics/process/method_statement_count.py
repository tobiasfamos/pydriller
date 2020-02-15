"""
Module that calculates the number of commits made to a file.
"""

from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

SUM_ADDED = "sum_statement_added"
MAX_ADDED = "max_statement_added"


def generate_method_long_name(file_name, method_long_name):
    return file_name + ":" + method_long_name


class MethodStatementCount(ProcessMetric):

    def count(self):
        methods = {}
        renamed_files = {}  # To keep track of renamed files

        for commit in RepositoryMining(path_to_repo=self.path_to_repo,
                                       from_commit=self.from_commit,
                                       to_commit=self.to_commit,
                                       reversed_order=True).traverse_commits():

            for modified_file in commit.modifications:

                file_path = renamed_files.get(modified_file.new_path, modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = file_path

                file_name = file_path.split("/")[-1]

                for method in modified_file.methods:
                    method_name = generate_method_long_name(file_name, method.long_name)
                    previous_added = methods.get(method_name, {SUM_ADDED: 0, MAX_ADDED: 0})
                    previous_added[SUM_ADDED] = previous_added[
                                                    SUM_ADDED] + method.statements_added
                    if previous_added[MAX_ADDED] < method.statements_added:
                        previous_added[MAX_ADDED] = method.statements_added
                    methods[method_name] = previous_added
        return methods
