from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.utils.DiffParser import get_changed_lines_between
from pydriller.utils.NameGenerator import generate_method_long_name


class MethodDeclarationCount(ProcessMetric):

    def count(self):
        methods = {}
        # last seen decl line: MethodDS
        renamed_files = {}
        renamed_methods = {}

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
                    add_line = ""
                    del_line = ""
                    declaration_lines = get_changed_lines_between(modified_file.diff, method.start_line,
                                                                  method.start_line)
                    if len(declaration_lines) == 0:
                        continue
                    for line in declaration_lines[:2]:
                        if line[1][0] == "+":
                            add_line = line[1]
                        else:
                            del_line = line[1]
                    current_method_ds = methods.pop(add_line[1:], MethodDS(method, add_line,
                                                                           generate_method_long_name(file_name,
                                                                                                     method.long_name)))
                    current_method_ds.change_decl(add_line, del_line)
                    methods[current_method_ds.last_decl_line] = current_method_ds

        return MethodDeclarationCount.__convert_return_value(methods)

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
