"""
Module that calculates the number of commits made to a file.
"""

from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric

SUM_ADDED = "sum_statement_added"
MAX_ADDED = "max_statement_added"


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
                    method_name = MethodStatementCount.__generate_method_long_name(file_name, method.long_name)
                    previous_added = methods.get(method_name, MethodStatementCount.__generate_empty_metrics())
                    previous_added = MethodStatementCount.__update_metrics(previous_added, method)
                    methods[method_name] = previous_added
        return methods

    @staticmethod
    def __update_metrics(metrics, method):
        metrics[SUM_ADDED] = metrics[
                                        SUM_ADDED] + method.statements_added
        if metrics[MAX_ADDED] < method.statements_added:
            metrics[MAX_ADDED] = method.statements_added
        return metrics

    @staticmethod
    def __generate_empty_metrics():
        return {SUM_ADDED: 0, MAX_ADDED: 0}

    @staticmethod
    def __generate_method_long_name(file_name, method_long_name):
        return file_name + ":" + method_long_name
