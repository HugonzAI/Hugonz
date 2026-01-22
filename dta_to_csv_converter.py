#!/usr/bin/env python3
"""
DTA to CSV Converter Module
Version: 1.0

Converts Fluke ESA615 .dta files to CSV format compatible with parse_fluke_file().

Output CSV format matches the structure expected by est_converter.py:
- Multi-column metadata format (Operator ID/Equipment Number on same row)
- Test Setup section
- Template Information section
- ESA615 Test Results table

Part of EST Converter V3.3 extension (produces equivalent input for core parser).
"""

import csv
import re


class DTAtoCSVConverter:
    """将.dta格式转换为Fluke CSV格式（兼容stable.txt）"""

    def __init__(self, dta_content):
        self.data = dta_content
        self.header = {}
        self.test_results = []
        self.applied_parts = []

    def parse(self):
        """解析.dta内容"""
        lines = self.data.split('\n')

        in_header = False
        in_body = False
        current_test = {}

        for line in lines:
            line = line.strip()

            if '<HEADER>' in line:
                in_header = True
                continue
            elif '<\\HEADER>' in line:
                in_header = False
                continue
            elif '<BODY>' in line:
                in_body = True
                continue
            elif '<\\BODY>' in line:
                in_body = False
                continue

            # 解析header - 只保留第一次出现（修复operator ID bug）
            if in_header and '=' in line:
                key, value = line.split('=', 1)
                if key not in self.header:
                    self.header[key] = value

            # 解析测试数据
            if in_body:
                if '<TEST=' in line or '<TESTAP=' in line:
                    if current_test and 'TestName' in current_test:
                        self.test_results.append(current_test)

                    test_match = re.search(r'<TEST(?:AP)?=(.+?)>', line)
                    if test_match:
                        current_test = {'TestName': test_match.group(1)}
                        if '<TESTAP=' in line:
                            current_test['IsAppliedPart'] = True

                elif '<\\TEST' in line:
                    if current_test and 'TestName' in current_test:
                        self.test_results.append(current_test)
                        current_test = {}

                elif current_test and ',' in line and not line.startswith('<'):
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 3:
                        if current_test.get('IsAppliedPart'):
                            current_test['APName'] = parts[0]
                            current_test['Limit'] = parts[1] if len(parts) > 1 else ''
                            current_test['Result'] = parts[3] if len(parts) > 3 else ''
                            current_test['Status'] = parts[4] if len(parts) > 4 else ''
                        else:
                            current_test['Limit'] = parts[0]
                            current_test['Result'] = parts[2]
                            current_test['Status'] = parts[3] if len(parts) > 3 else ''

        # 解析Applied Parts
        ap_names = self.header.get('APNAME', '').split(',')
        ap_types = self.header.get('APTYPE', '').split(',')
        ap_nums = self.header.get('NUMAP', '').split(',')

        for i in range(len(ap_names)):
            if ap_names[i].strip():
                self.applied_parts.append({
                    'name': ap_names[i].strip(),
                    'type': ap_types[i].strip() if i < len(ap_types) else '',
                    'num': ap_nums[i].strip() if i < len(ap_nums) else ''
                })

        return self.header, self.test_results

    def to_csv(self, output_file):
        """转换为CSV - 输出格式完全兼容stable.txt的parse_fluke_file()"""
        self.parse()

        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)

            # Test Setup Header
            writer.writerow(['Test Setup', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', 'DUT Information', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])

            # Operator and DUT info (multi-column format - critical for parser compatibility)
            writer.writerow(['Operator ID :', '', self.header.get('ESA615OPID', ''), '',
                           'Equipment Number :', '', self.header.get('DUTEQUIPNUM', ''), ''])
            writer.writerow(['Calibration Tech :', '', self.header.get('ESA615CALTECH', ''), '',
                           'Serial Number :', '', self.header.get('DUTSN', ''), ''])

            # Calibration Date formatting
            cal_date = self.header.get('ESA615CALDATE', '')
            if cal_date.startswith('M') and 'D' in cal_date and 'Y' in cal_date:
                try:
                    m = int(cal_date[1:3])
                    d = int(cal_date[4:6])
                    y = cal_date[7:11]
                    cal_date = f"{m}/{d}/{y}"
                except:
                    pass

            writer.writerow(['Calibration Date :', '', cal_date, '',
                           'Manufacturer :', '', self.header.get('DUTMANF', ''), ''])
            writer.writerow(['Firmware Version :', '', self.header.get('ESA615UIFW', ''), '',
                           'Model :', '', self.header.get('DUTMODEL', ''), ''])
            writer.writerow(['Serial Number :', '', self.header.get('ESA615SN', ''), '',
                           'Location :', '', self.header.get('DUTLOC', ''), ''])

            # Date & Time formatting (critical for parser)
            date_str = self.header.get('DATEOFTEST', '')
            time_str = self.header.get('TIMEOFTEST', '')
            try:
                date_parts = date_str.split('/')
                if len(date_parts) == 3:
                    datetime_str = f"{int(date_parts[1])}/{int(date_parts[2])}/{date_parts[0]} {time_str}"
                else:
                    datetime_str = f"{date_str} {time_str}"
            except:
                datetime_str = f"{date_str} {time_str}"

            writer.writerow(['Date & Time :', '', datetime_str, '',
                           'Other :', '', self.header.get('OTHER', ''), ''])
            writer.writerow(['JOB Name :', '', '', '', '', '', '', ''])

            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])

            # Template Information
            writer.writerow(['Template Information', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])

            writer.writerow(['Template Name :', '', self.header.get('MASTERFILE', ''), '',
                           'Standard :', '', self.header.get('STANDARD', ''), ''])
            writer.writerow(['Pause after Power ON:', '', self.header.get('PAUSEAFTERON', 'NO'), '',
                           'Pause before Power OFF:', '', self.header.get('PAUSEBEFOREOFF', 'NO'), ''])
            writer.writerow(['Power ON delay:', '', self.header.get('PONDELAY', '1'), '',
                           'Power OFF delay:', '', self.header.get('POFFDELAY', '0'), ''])
            writer.writerow(['Test Speed:', '', self.header.get('TSPEED', 'RAPID'), '',
                           'Test Mode:', '', self.header.get('TMODE', 'AUTO'), ''])
            writer.writerow(['Halt on Test Failure:', '', self.header.get('HALTONFAIL', 'YES'), '',
                           'Multiple PE Test:', '', self.header.get('MULTIPETEST', 'YES'), ''])
            writer.writerow(['Include Time:', '', self.header.get('INCLUDETIME', 'YES'), '',
                           'Patient Lead Record:', '', self.header.get('MULTIRESSTORE', 'WORST/LAST'), ''])
            writer.writerow(['Insulation Resistance Voltage:', '', self.header.get('INSVOLTAGE', '500V'), '',
                           'Reverse Polarity:', '', self.header.get('REVERSEPOL', 'YES'), ''])
            writer.writerow(['Multiple Non-Earth Leakage:', '', self.header.get('MULTIENCLTEST', 'YES'), '',
                           'Classification:', '', self.header.get('CLASSIFICATION', 'I'), ''])

            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])

            # Applied part setup
            writer.writerow(['PLC Configuration-Applied part setup', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['AP Name', 'AP Type', 'AP Num', '', '', '', '', ''])

            for ap in self.applied_parts:
                writer.writerow([ap['name'], ap['type'], ap['num'], '', '', '', '', ''])

            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])

            # ESA615 Test Results
            writer.writerow(['ESA615 Test Results', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['Test Name', '', '', '', 'Value', 'High Limits', 'Low Limits', 'Status'])
            writer.writerow(['', '', '', '', '', '', '', ''])

            # 写入测试结果 - 简化版本，保证与stable.txt兼容
            for test in self.test_results:
                test_name = test.get('TestName', '')
                # 跳过消息类测试
                if 'MSGE' in test_name or test_name in ['LOAD601', 'GFI10']:
                    continue

                writer.writerow([
                    test_name, '', '',
                    test.get('APName', ''),
                    test.get('Result', ''),
                    test.get('Limit', ''),
                    '',
                    test.get('Status', '')
                ])

            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '________', '', ''])
            writer.writerow(['', '', '', '', '', 'Signature', '', ''])
