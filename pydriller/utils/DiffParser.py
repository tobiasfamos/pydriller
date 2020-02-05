def get_changed_lines_between(diff, start_line, end_line):
    hunk_string = diff.split("@@")[1]
    hunk = Hunk.create_from_string(hunk_string)
    diff_split_by_lines = diff.split("\n")
    line_count = hunk.from_after - 1
    line_list = []
    for line in diff_split_by_lines:
        if line and (line[0] == "-" or line[0] == "+"):
            if start_line <= line_count <= end_line:
                line_list.append([line_count, line])
            if line[0] == '-':
                line_count -= 1
        line_count += 1
    return line_list
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
