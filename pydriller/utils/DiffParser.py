import re

def get_changed_lines_between(diff, start_line, end_line):
    hunk_diff_list = get_hunks_and_diffs(diff)
    line_list = []
    for hunk_diff_pair in hunk_diff_list:
        hunk_string = hunk_diff_pair[0].split("@@")[1]
        hunk = Hunk.create_from_string(hunk_string)
        diff_split_by_lines = hunk_diff_pair[1].split("\n")
        line_count = hunk.from_after - 1
        for line in diff_split_by_lines:
            if line and (line[0] == "-" or line[0] == "+"):
                if start_line <= line_count <= end_line:
                    line_list.append([line_count, line])
                if line[0] == '-':
                    line_count -= 1
            line_count += 1
    return line_list

def get_hunks_and_diffs(diff):
    splitted = re.split('(@@ -\d+,\d+ \+\d+,\d+ @@)',diff)
    splitted.pop(0)
    hunk_diff_list = []
    hunks = splitted[::2]
    diffs= splitted[1::2]
    for i in range(0, len(hunks)):
        hunk_diff_list.append([hunks[i], diffs[i]])
    return hunk_diff_list



class Hunk:
    def __init__(self, from_before, no_lines_before, from_after, no_lines_after):
        self.from_before = int(from_before)
        self.no_lines_before = int(no_lines_before)
        self.from_after = int(from_after)
        self.no_lines_after = int(no_lines_after)

    @staticmethod
    def create_from_string(string):
        splited = string.strip().split("+")
        return Hunk(splited[0].split(",")[0].strip("-"), splited[0].split(",")[1], splited[1].split(",")[0],
                    splited[1].split(",")[1])
