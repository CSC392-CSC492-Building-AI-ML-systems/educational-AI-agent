from parse_data_abdullah import *
import pytest

def test_output_tag():
    final = []

    filename = "tests/input_files/output_tag_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files")
    final.extend(finals)

    print(final)

    assert final[0]['User'] == """<data-piece><history></history><current-entry><entry><input></input><output>Linux boxtop 6. 6. 13-amd64 1 SMP PREEMPT_DYNAMIC Debian 6. 6. 13-1 (2024-01-20) x86_64Plan your installation, and FAI installs your plan. Last login Sun Sep 22 122417 2024</output><annotation>[BLANK]</annotation></entry></current-entry></data-piece>"""

if __name__ == '__main__':
    pytest.main(['scripts/parse_data_abdullah_test.py'])