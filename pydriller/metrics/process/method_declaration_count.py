from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.utils.DiffParser import get_changed_lines_between
from pydriller.utils.MethodIterator import get_methods_reversed
from pydriller.utils.NameGenerator import generate_method_long_name


class MethodDeclarationCount(ProcessMetric):
    def __init__(self, path_to_repo: str,
                 from_commit: str,
                 to_commit: str):
        super().__init__(path_to_repo, from_commit, to_commit)
        self.methods = {}
        # last seen decl line: MethodDS

    def count(self):
        self.methods = {}
        for method in get_methods_reversed(self.path_to_repo, self.from_commit, self.to_commit):
            self.__handle_method(method)

        return MethodDeclarationCount.__convert_return_value(self.methods)

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

    @staticmethod
    def __convert_return_value(methods):
        metrics = {}
        for method in methods.values():
            metrics[method.method_long_name] = method.decl_changes
        return metrics

    def __handle_method(self, method_dto):
        add_line = ""
        del_line = ""
        declaration_lines = get_changed_lines_between(method_dto.modified_file.diff, method_dto.method.start_line,
                                                      method_dto.method.start_line)
        if len(declaration_lines) == 0:
            return
        for line in declaration_lines[:2]:
            if line[1][0] == "+":
                add_line = line[1]
            else:
                del_line = line[1]
        current_method_ds = self.methods.pop(add_line[1:], MethodDS(method_dto, add_line, method_dto.method_long_name))
        current_method_ds.change_decl(add_line, del_line)
        self.methods[current_method_ds.last_decl_line] = current_method_ds


class MethodDS:
    def __init__(self, method, last_decl_line, method_long_name):
        self.method = method
        self.decl_changes = 0
        self.last_decl_line = last_decl_line
        self.method_long_name = method_long_name

    def change_decl(self, add_line, del_line):
        self.decl_changes += 1
        if del_line == "":
            self.last_decl_line = add_line[1:]
        else:
            self.last_decl_line = del_line[1:]
