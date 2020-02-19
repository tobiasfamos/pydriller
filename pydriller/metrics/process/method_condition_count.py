from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric
from pydriller.utils.DiffParser import get_changed_lines_between
from pydriller.utils.NameGenerator import generate_method_long_name
import re

COND_CHANGES = "condition_changes"
REGEX_CONDITION = r"(if\s*\(.+\))"


class MethodConditionCount(ProcessMetric):
    def __init__(self, path_to_repo: str,
                 from_commit: str,
                 to_commit: str):
        super().__init__(path_to_repo, from_commit, to_commit)
        self.methods = {}

    def count(self):
        self.methods = {}
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
                    method_long_name_with_file = generate_method_long_name(file_name, method.long_name)
                    self.__handle_method(modified_file, method, method_long_name_with_file)

        return self.methods

    def __handle_method(self, modified_file, method, method_long_name):
        method_diff = get_changed_lines_between(modified_file.diff, method.start_line, method.end_line)
        changed_conditions = set()
        for line in method_diff:
            line_diff = line[1]
            if re.findall(REGEX_CONDITION, line_diff):
                changed_conditions.add(line[0])
        previous_condition_changes = self.methods.get(method_long_name,
                                                      MethodConditionCount.__generate_empty_metrics())
        previous_condition_changes[COND_CHANGES] += len(changed_conditions)
        self.methods[method_long_name] = previous_condition_changes

    @staticmethod
    def __generate_empty_metrics():
        return {COND_CHANGES: 0}
