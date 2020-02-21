from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.utils.MethodIterator import get_methods_reversed
from pydriller.utils.NameGenerator import generate_method_long_name


class MethodAuthorCount(ProcessMetric):

    def __init__(self, path_to_repo: str,
                 from_commit: str,
                 to_commit: str):
        super().__init__(path_to_repo, from_commit, to_commit)
        self.methods = {}

    def count(self):
        self.methods = {}
        for method in get_methods_reversed(self.path_to_repo, self.from_commit, self.to_commit):
            self.__hanlde_method(method)
        return MethodAuthorCount.__create_return_metrics(self.methods)

    @staticmethod
    def __create_return_metrics(methods):
        metrics = {}
        for method_long_name in methods.keys():
            metrics[method_long_name] = len(methods[method_long_name])
        return metrics

    @staticmethod
    def __add_author_to_method_list(methods, author, method_long_name_with_file):
        method = methods.get(method_long_name_with_file, set())
        method.add(author)
        methods[method_long_name_with_file] = method

    def __hanlde_method(self, method_dto):
        if method_dto.method.statements_deleted or method_dto.method.statements_added:
            MethodAuthorCount.__add_author_to_method_list(self.methods, method_dto.commit.author,
                                                          method_dto.method_long_name)
