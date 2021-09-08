# This is a sample Python script.
import sys
import os


def check_line(line: str):
    """
    this function checking format
    :param line: str line in file
    :return: boolean
    """
    return len(line.split('dut:')) == 2


def check_file(file: str):
    """
    checking file existence
    :param file: string path of file
    :return: boolean
    """
    if not os.path.isfile(file):
        print('you need give the correct path of file')
        return False
    return True


def parse_line(line: str):
    """
    function parsing a line and return the status and date
    :param line: string  line to parse
    :return: (string, string) | bool
    """
    if check_line(line):
        line = line.replace('\n', '')
        date = line.split('dut:')[0].strip()
        status = line.split('dut:')[1].split(':')[1].strip()
        return date, status
    return False


def parse_file(file: str):
    """
    function parsing a file
    :param file: string file to parse
    :return: list
    """
    lines = []
    if check_file(file):
        with open(file, 'r') as f:
            for line in f.readlines():
                if check_line(line):
                    lines.append(parse_line(line))
    return lines


def check_row(line: str):
    """
    function checking the format of row
    :param line: string line to check
    :return: boolean
    """
    return len(line) == 2


def report_activity(lines: list):
    """
    function reporting the device activity
    :param lines: list lines parsed from files
    :return: list, list
    """
    errors_times = []
    on_times = []
    first_time_on = ''
    for line in lines:
        if check_row(line):
            date = line[0]
            status = line[1]
            if status == 'ERR':
                errors_times.append(date)
                first_time_on = ''
            elif status == 'ON':
                if first_time_on == '':
                    first_time_on = date
                    on_times.append([first_time_on, first_time_on])
                on_times[-1][1] = date
            else:
                first_time_on = ''
    return on_times, errors_times


def print_report(on_times: list, err_times: list):
    """
    function logging report activity to console
    :param on_times: list all lines when the device was on
    :param err_times: list all lines when the device was err
    """
    for on_time in on_times:
        print('the device was on from', on_time[0], 'to', on_time[1])
    for err_time in err_times:
        print('the device has err on : ' + err_time)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('you need to specify a file')
        print('you need run the script like this: python logparser.py [file_path]')
        sys.exit()
    file = sys.argv[1]
    lines = parse_file(file)
    on_times_report, err_times_report = report_activity(lines)
    print_report(on_times_report, err_times_report)
