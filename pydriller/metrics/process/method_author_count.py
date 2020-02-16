from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.utils.NameGenerator import generate_method_long_name


class MethodAuthorCount(ProcessMetric):

    def count(self):
        methods = {}
        renamed_files = {}

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
                    if method.statements_deleted or method.statements_added:
                        method_long_name_with_file = generate_method_long_name(file_name, method.long_name)
                        MethodAuthorCount.__add_author_to_method_list(methods, commit.author,
                                                                      method_long_name_with_file)

        return MethodAuthorCount.__create_return_metrics(methods)

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
