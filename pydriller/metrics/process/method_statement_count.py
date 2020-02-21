from pydriller.domain.commit import ModificationType
from pydriller.repository_mining import RepositoryMining
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.utils.MethodIterator import get_methods_reversed
from pydriller.utils.NameGenerator import generate_method_long_name

SUM_ADDED = "sum_statement_added"
MAX_ADDED = "max_statement_added"
AVG_ADDED = "average_statement_added"
NUM_MODIFIED = "method_histories"
SUM_DELETED = "sum_statement_deleted"
MAX_DELETED = "max_statement_deleted"
AVG_DELETED = "average_statement_deleted"
CHURN = "churn"
AVG_CHURN = "average_churn"
MAX_CHURN = "max_churn"


class MethodStatementCount(ProcessMetric):

    def __init__(self, path_to_repo: str,
                 from_commit: str,
                 to_commit: str):
        super().__init__(path_to_repo, from_commit, to_commit)
        self.methods = {}

    def count(self):
        self.methods = {}
        for method in get_methods_reversed(self.path_to_repo, self.from_commit, self.to_commit):
            self.__handle_method(method)
        return MethodStatementCount.__create_return_metrics(self.methods)

    def __handle_method(self, method_dto):
        previous_added = self.methods.get(method_dto.method_long_name, MethodStatementCount.__generate_empty_metrics())
        previous_added = MethodStatementCount.__update_metrics(previous_added, method_dto.method)
        self.methods[method_dto.method_long_name] = previous_added

    @staticmethod
    def __update_metrics(metrics, method):
        metrics[SUM_ADDED] = metrics[SUM_ADDED] + method.statements_added
        metrics[SUM_DELETED] = metrics[SUM_DELETED] + method.statements_deleted
        if metrics[MAX_ADDED] < method.statements_added:
            metrics[MAX_ADDED] = method.statements_added
        if metrics[MAX_DELETED] < method.statements_deleted:
            metrics[MAX_DELETED] = method.statements_deleted
        if method.statements_added or method.statements_deleted:
            metrics[NUM_MODIFIED] += 1
        if method.statements_added - method.statements_deleted > metrics[MAX_CHURN]:
            metrics[MAX_CHURN] = method.statements_added - method.statements_deleted
        return metrics

    @staticmethod
    def __generate_empty_metrics():
        return {SUM_ADDED: 0, MAX_ADDED: 0, NUM_MODIFIED: 0, SUM_DELETED: 0, MAX_DELETED: 0, MAX_CHURN: 0}

    @staticmethod
    def __create_return_metrics(methods):
        metrics = {}
        for method_name in methods:
            metrics[method_name] = {
                SUM_ADDED: methods[method_name][SUM_ADDED],
                MAX_ADDED: methods[method_name][MAX_ADDED],
                SUM_DELETED: methods[method_name][SUM_DELETED],
                MAX_DELETED: methods[method_name][MAX_DELETED],
                NUM_MODIFIED: methods[method_name][NUM_MODIFIED],
                MAX_CHURN: methods[method_name][MAX_CHURN]

            }
        metrics = MethodStatementCount.__add_absolutes(metrics)
        metrics = MethodStatementCount.__add_averages(metrics)
        return metrics

    @staticmethod
    def __add_averages(methods):
        for method in methods.values():
            if method[NUM_MODIFIED] == 0:
                method[AVG_ADDED] = 0
                method[AVG_DELETED] = 0
                method[AVG_CHURN] = 0
            else:
                method[AVG_ADDED] = method[SUM_ADDED] / method[NUM_MODIFIED]
                method[AVG_DELETED] = method[SUM_DELETED] / method[NUM_MODIFIED]
                method[AVG_CHURN] = method[CHURN] / method[NUM_MODIFIED]
        return methods

    @staticmethod
    def __add_absolutes(methods):
        for method in methods.values():
            method[CHURN] = method[SUM_ADDED] - method[SUM_DELETED]
        return methods
