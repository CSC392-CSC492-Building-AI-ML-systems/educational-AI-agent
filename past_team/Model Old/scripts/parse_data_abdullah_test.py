from parse_data_abdullah import *
import pytest

def test_output_tag():
    """
    Test the output XML tag
    """
    final = []

    filename = "tests/input_files/output_tag_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/output_test")
    final.extend(finals)

    assert final[-1]['prompt'] == "<data-piece>" + \
                                    "<history></history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input></input>" + \
                                            "<output>Linux boxtop 6.6.13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.6.13-1 (2024-01-20) x86_64\r\n\r\n\r\nPlan your installation, and FAI installs your plan.\r\n\r\nLast login: Sun Sep 22 12:24:17 2024</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"
    
def test_input_tag():
    """
    Test the input XML tag.
    """
    final = []

    filename = "tests/input_files/input_tag_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/input_test")
    final.extend(finals)

    assert final[-1]['prompt'] == "<data-piece>" + \
                                    "<history></history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input>ssh 10.0.7.138</input>" + \
                                            "<output>ssh 10.0.7.138\r\n\x1b[?2004l</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"

def test_chosen():
    """
    Test chosen key in output.
    """
    final = []

    filename = "tests/input_files/chosen_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/chosen_test")
    final.extend(finals)

    assert final[-1]['prompt'] == "<data-piece>" + \
                                    "<history></history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input>ssh 10.0.7.138</input>" + \
                                            "<output>ssh 10.0.7.138</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"

    assert final[-1]['chosen'] == 'ssh into server at 10.0.7.138'

def test_chosen_no_annotation():
    """
    Test the chosen key when there is no annotation in the current data piece.
    """
    final = []

    filename = "tests/input_files/no_chosen_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/no_chosen_test")
    final.extend(finals)

    assert final[-1]['prompt'] == "<data-piece>" + \
                                    "<history></history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input>ls -larth</input>" + \
                                            "<output>ls -larth\r\n\x1b[?2004l</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"

    assert final[-1]['chosen'] == '[NO_OUTPUT]'

def test_history_tag():
    """
    Test the history tag.
    """
    final = []

    filename = "tests/input_files/history_tag_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/input_test")
    final.extend(finals)

    assert final[-1]['prompt'] == "<data-piece>" + \
                                    "<history>" + \
                                        "<entry>" + \
                                            "<input></input>" + \
                                            "<output>\x1b[?2004h\x1b]0;demo@boxtop: ~\x07demo@boxtop:~$</output>" + \
                                            "<annotation></annotation>" + \
                                        "</entry>" + \
                                    "</history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input>ssh 10.0.7.138</input>" + \
                                            "<output>ssh 10.0.7.138</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"

    assert final[-1]['chosen'] == 'ssh into server at 10.0.7.138'

def test_annotation_tag():
    """
    Test the annotation tag for an annotation session using only one depth.
    """
    final = []

    filename = "tests/input_files/annotation_tag_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/annotation_test")
    final.extend(finals)

    print(final)

    assert final[-1]['prompt'] == "<data-piece>" + \
                                    "<history>" + \
                                        "<entry>" + \
                                            "<input>ls -larth</input>" + \
                                            "<output>ls -larth\r\n\x1b[?2004l</output>" + \
                                            "<annotation>listed out the contents of this directory</annotation>" + \
                                        "</entry>" + \
                                    "</history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input>sudo apt install asciinema\r1M3T567!</input>" + \
                                            "<output>sudo apt install asciinema\r\n\x1b[?2004l\r[sudo] password for demo:</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"

def test_annotation_depth_tags():
    """
    Test the annotation tags when multiple depths are used.
    """
    final = []

    filename = "tests/input_files/annotation_tag_depth_test.annotated"
    finals = parse_and_save_file(filename, "tests/output_files/annotation_depth_test")
    final.extend(finals)

    assert final[0]['prompt'] == "<data-piece>" + \
                                    "<history></history>" + \
                                    "<current-entry>" + \
                                        "<entry>" + \
                                            "<input>\x1b[200~ssh bandit12@bandit.labs.overthewire.org -p 2220\x1b[201~</input>" + \
                                            "<output>\x1b[?2004h\x1b]0;renee_k@Renee: ~\x07\x1b[01;32mrenee_k@Renee\x1b[00m:\x1b[01;34m~\x1b[00m$</output>" + \
                                            "<annotation>[BLANK]</annotation>" + \
                                            "<annotation>Subgoal: Type in the ssh password for user bandit12 correctly</annotation>" + \
                                            "<annotation>successResult</annotation>" + \
                                            "<annotation>Tools: The ssh tool from OpenSSH</annotation>" + \
                                        "</entry>" + \
                                    "</current-entry>" + \
                                "</data-piece>"
    
    assert final[1]['prompt'] == "<data-piece>" + \
                                "<history></history>" + \
                                "<current-entry>" + \
                                    "<entry>" + \
                                        "<input>\x1b[200~ssh bandit12@bandit.labs.overthewire.org -p 2220\x1b[201~</input>" + \
                                        "<output>\x1b[?2004h\x1b]0;renee_k@Renee: ~\x07\x1b[01;32mrenee_k@Renee\x1b[00m:\x1b[01;34m~\x1b[00m$</output>" + \
                                        "<annotation>Goal: ssh into bandit12@bandit.labs.overthewire.org on port 2220</annotation>" + \
                                        "<annotation>[BLANK]</annotation>" + \
                                        "<annotation>successResult</annotation>" + \
                                        "<annotation>Tools: The ssh tool from OpenSSH</annotation>" + \
                                    "</entry>" + \
                                "</current-entry>" + \
                            "</data-piece>"

    assert final[2]['prompt'] == "<data-piece>" + \
                                "<history></history>" + \
                                "<current-entry>" + \
                                    "<entry>" + \
                                        "<input>\x1b[200~ssh bandit12@bandit.labs.overthewire.org -p 2220\x1b[201~</input>" + \
                                        "<output>\x1b[?2004h\x1b]0;renee_k@Renee: ~\x07\x1b[01;32mrenee_k@Renee\x1b[00m:\x1b[01;34m~\x1b[00m$</output>" + \
                                        "<annotation>Goal: ssh into bandit12@bandit.labs.overthewire.org on port 2220</annotation>" + \
                                        "<annotation>Subgoal: Type in the ssh password for user bandit12 correctly</annotation>" + \
                                        "<annotation>[BLANK]</annotation>" + \
                                        "<annotation>Tools: The ssh tool from OpenSSH</annotation>" + \
                                    "</entry>" + \
                                "</current-entry>" + \
                            "</data-piece>"
        
    assert final[3]['prompt'] == "<data-piece>" + \
                                "<history></history>" + \
                                "<current-entry>" + \
                                    "<entry>" + \
                                        "<input>\x1b[200~ssh bandit12@bandit.labs.overthewire.org -p 2220\x1b[201~</input>" + \
                                        "<output>\x1b[?2004h\x1b]0;renee_k@Renee: ~\x07\x1b[01;32mrenee_k@Renee\x1b[00m:\x1b[01;34m~\x1b[00m$</output>" + \
                                        "<annotation>Goal: ssh into bandit12@bandit.labs.overthewire.org on port 2220</annotation>" + \
                                        "<annotation>Subgoal: Type in the ssh password for user bandit12 correctly</annotation>" + \
                                        "<annotation>successResult</annotation>" + \
                                        "<annotation>[BLANK]</annotation>" + \
                                    "</entry>" + \
                                "</current-entry>" + \
                            "</data-piece>"

def test_chosen_multiple_depth():
    """
    Test the chosen key in different data pieces when there are multiple depths of annotations.
    """
    final = []

    filename = "tests/input_files/annotation_tag_depth_test.annotated" # same file as previous test case
    finals = parse_and_save_file(filename, "tests/output_files/chosen_depth_test")
    final.extend(finals)

    # each chosen's annotation is one depth deeper then the previous one
    chosens = ["Goal: ssh into bandit12@bandit.labs.overthewire.org on port 2220",
                "Subgoal: Type in the ssh password for user bandit12 correctly",
                "successResult", "Tools: The ssh tool from OpenSSH"]

    for i in range(len(chosens)):
        assert final[i]['chosen'] == chosens[i]

if __name__ == '__main__':
    pytest.main(['scripts/parse_data_abdullah_test.py'])