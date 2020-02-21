from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from pydriller.utils.NameGenerator import generate_method_long_name


def get_methods_reversed(path_to_repo, from_commit, to_commit):
    methods = {}
    renamed_files = {}

    for commit in RepositoryMining(path_to_repo=path_to_repo,
                                   from_commit=from_commit,
                                   to_commit=to_commit,
                                   reversed_order=True).traverse_commits():

        for modified_file in commit.modifications:

            file_path = renamed_files.get(modified_file.new_path, modified_file.new_path)

            if modified_file.change_type == ModificationType.RENAME:
                renamed_files[modified_file.old_path] = file_path

            file_name = file_path.split("/")[-1]

            for method in modified_file.methods:
                method_long_name = generate_method_long_name(file_name, method.long_name)
                yield MethodDTO(modified_file, method, method_long_name, commit)


class MethodDTO:
    def __init__(self, modified_file, method, method_long_name, commit):
        self.modified_file = modified_file
        self.method = method
        self.method_long_name = method_long_name
        self.commit = commit
