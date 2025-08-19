import re
from typing import List, Optional, Tuple, Dict

_GROUP_RE = re.compile(r'\bgroup\s*=\s*(?:"|\')(\d+)(?:"|\')', re.IGNORECASE)
_SORTME_RE = re.compile(r'\bsortme\s*=\s*(?:"|\')([^"\']+)(?:"|\')', re.IGNORECASE)
_ANSWER_RE = re.compile(r'^\s*Answer:\s*([^\s\n]+)', re.IGNORECASE | re.MULTILINE)
_DATA_RE = re.compile(r"<data>\s*(?P<body><.*>)\s*</data>", re.IGNORECASE | re.DOTALL)
_TS_RE = re.compile(r'timestamp\s*=\s*"([^"]+)"', re.IGNORECASE)
SEGMENTS_MAP = {}

def _extract_data(text):
    """
    Extract input data from the model input.
    """
    if not text:
        return None
    m = _DATA_RE.search(text)
    return m.group(1) if m else None

def _get_timestamps(lines):
        out = []
        for line in lines:
            m = _TS_RE.search(line)
            out.append(m.group(1) if m else None)
        return out

def _find_overlap(a, b):
    """
    Return the length of the longest overlap between the end of list a and the start of list b according to their timestamps.
    """
    a = _get_timestamps(a)
    b = _get_timestamps(b)
    max_k = min(len(a), len(b))
    for k in range(max_k, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0

def _append_line(seg_map, gid, line_num):
    """
    Append line number to the segment map for the given group ID.
    """
    if gid is None:
        return
    if gid not in seg_map:
        seg_map[gid] = []
    seg_map[gid].append(line_num)


def _current_max_gid(seg_map, current_group):
    """
    Get the maximum group ID from the segment map.
    """
    keys = list(seg_map.keys())
    if current_group is not None:
        keys.append(current_group)
    return max(keys) if keys else None


def extract_gid(line):
    """
    Extract group ID from a line.
    """
    if not line:
        return None
    m = _GROUP_RE.search(line)
    if not m:
        return None
    try:
        val = int(m.group(1))
        return val if val >= 0 else None
    except Exception:
        return None


def has_sortme(line):
    """
    Check if the line contains 'sortme' attribute.
    """
    if not line:
        return False
    m = _SORTME_RE.search(line)
    return True if m else False


def answer_to_label(model_output):
    """
    Parse the answer from the model output into label.
    """
    if not model_output:
        return None
    m = _ANSWER_RE.search(model_output)
    if not m:
        return None
    answer = m.group(1).strip()
    if answer.upper() == "NEW":
        return -1
    try:
        label = int(answer)
        if label >= 0:
            return label
    except Exception:
        return None
    return None  # negative label


def convert_to_segments(lines, model_output, start_line=1):
    """
    Convert a paired model input and model output into predicted segments.
    """
    current_group = None
    sortme_seen = False
    final_group_num = None
    sortme_group_num = None

    for idx, line in enumerate(lines, start=start_line):
        if not sortme_seen:
            if not has_sortme(line):
                g = extract_gid(line)
                if g is not None:
                    current_group = g
                _append_line(SEGMENTS_MAP, current_group, idx)

            else:
                sortme_seen = True
                final_group_num = _current_max_gid(SEGMENTS_MAP, current_group)

                label = answer_to_label(model_output)
                if label:
                    if label == -1:
                        sortme_group_num = (final_group_num + 1) if final_group_num is not None else 0
                    else:
                        sortme_group_num = label
                else:
                    raise ValueError("Model output does not contain a valid answer.")  
                _append_line(SEGMENTS_MAP, sortme_group_num, idx)

        else:
            _append_line(SEGMENTS_MAP, sortme_group_num, idx)

def get_pred_segments(inputs, outputs):
    """
    Convert multiple paired model inputs and model outputs into a list of predicted segments.
    """
    if len(inputs) != len(outputs):
        raise ValueError("Inputs and outputs must be paired and have the same length.")
    
    prev_lines = None
    offset = 1  # line number of the last processed input
    for input, output in zip(inputs, outputs):
        curr_lines = _extract_data(input).splitlines()
        if prev_lines:
            k = _find_overlap(prev_lines, curr_lines)
        else:
            k = 0

        convert_to_segments(curr_lines[k:], output, start_line=offset)
        offset = offset + len(curr_lines[k:])
        prev_lines = curr_lines
    return [SEGMENTS_MAP[k] for k in sorted(SEGMENTS_MAP.keys())]