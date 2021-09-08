import io
import sys
import unittest.mock
import pathlib
import logparse


class MyTestCase(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, func, mock_stdout, **kwargs):
        func(**kwargs)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_checkline(self):
        line = 'Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON'
        self.assertEqual(logparse.check_line(line), True)  # add assertion here
        line = 'This line is not correct'
        self.assertEqual(logparse.check_line(line), False)

    def test_check_row(self):
        self.assertEqual(logparse.check_row(('Jul 11 16:11:51:490 [139681125603136]', 'ON')), True)
        self.assertEqual(logparse.check_row('Jul 11 16:11:51:490 [139681125603136]'), False)

    def test_parse_file(self):
        self.assert_stdout(
            'you need give the correct path of file\n',
            logparse.check_file,
            {'file': str(pathlib.Path(__file__).parent.resolve()) + '/testlogs.txt'}
        )
        self.assertEqual(logparse.check_file(str(pathlib.Path(__file__).parent.resolve()) + '/testlogs'), True)

    def test_parse_line(self):
        line = 'Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON'
        expected_result = 'Jul 11 16:11:51:490 [139681125603136]', 'ON'
        self.assertEqual(logparse.parse_line(line), expected_result)
        line = 'ONE POINT GROUP'
        self.assertEqual(logparse.parse_line(line), False)

    def test_parse_file(self):
        expectedlines = [
            ('Jul 11 16:11:51:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:52:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:53:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:54:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:55:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:55:490 [139681125603136]', 'OFF')
        ]
        self.assertEqual(logparse.parse_file(str(pathlib.Path(__file__).parent.resolve()) + '/testlogs'), expectedlines)

    def test_report_activity(self):
        expect_result = [
            ['Jul 11 16:11:51:490 [139681125603136]', 'Jul 11 16:11:55:490 [139681125603136]'],
            ['Jul 11 16:11:57:490 [139681125603136]', 'Jul 11 16:11:57:490 [139681125603136]']
        ], [
            'Jul 11 16:11:58:490 [139681125603136]'
        ]
        lines = [
            ('Jul 11 16:11:51:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:52:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:53:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:54:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:55:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:56:490 [139681125603136]', 'OFF'),
            ('Jul 11 16:11:57:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:58:490 [139681125603136]', 'ERR')
        ]
        self.assertEqual(logparse.report_activity(lines), expect_result)
        expect_result = [
                            ['Jul 11 16:11:51:490 [139681125603136]', 'Jul 11 16:11:55:490 [139681125603136]'],
                            ['Jul 11 16:11:57:490 [139681125603136]', 'Jul 11 16:11:57:490 [139681125603136]']
                        ], [
                            'Jul 11 16:11:58:490 [139681125603136]'
                        ]
        lines = [
            ('Jul 11 16:11:51:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:52:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:53:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:54:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:55:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:56:490 [139681125603136]', 'OFF'),
            ('Jul 11 16:11:57:490 [139681125603136]', 'ON'),
            ('Jul 11 16:11:58:490 [139681125603136]', 'ERR'),
            'NO CORRECT',
            'NO'
        ]
        self.assertEqual(logparse.report_activity(lines), expect_result)

    def test_print_report(self):
        on_times, err_times = [
                                  ['Jul 11 16:11:51:490 [139681125603136]', 'Jul 11 16:11:55:490 [139681125603136]'],
                              ], \
                              [
                                  'Jul 11 16:11:58:490 [139681125603136]'
                              ]
        expected_output = 'the device was on from Jul 11 16:11:51:490 [139681125603136] to Jul 11 16:11:55:490 [139681125603136]\nthe device has err on : Jul 11 16:11:58:490 [139681125603136]\n'
        args = {'on_times': on_times, 'err_times': err_times}
        self.assert_stdout(expected_output, logparse.print_report, **args)


if __name__ == '__main__':
    unittest.main()
