
# ======== Helpers ========
def _gt_segments(gt_file):
    """
    Read ground truth segments from a file.
    
    :param gt_file: Path to the ground truth file.
    :return: List of segments.
    """
    segments = []
    current = []

    with open(gt_file, "r") as f:
        for line in f:
            n = int(line.strip())
            if n == 0:
                if current:
                    segments.append(current)
                    current = []
            else:
                current.append(n)
    return segments

def _segments_to_boundaries(segments):
    starts = sorted(min(seg) for seg in segments if seg)
    return starts[1:] if len(starts) >= 2 else []

def _to_sets(segments):
    return [set(seg) for seg in segments]

def _iou(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0

def _greedy_match(pred, gt, k=0):
    """
    Greedily match predicted boundaries to ground truth boundaries with tolerance k.
    Each ground truth boundary can be matched at most once.

    :return: number of matched boundaries.
    """
    gt_used = [False] * len(gt)
    matches = 0

    for p in sorted(pred):
        best_i = -1
        best_dist = None

        # Find the closest unused ground truth boundary within tolerance k
        for i, g in enumerate(sorted(gt)):
            if gt_used[i]:
                continue
            dist = abs(p - g)
            if dist <= k:  # tolerance
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_i = i
        if best_i >= 0:
            gt_used[best_i] = True
            matches += 1
    return matches

# ======== Segmentation-Level Metrics ========
def _pred2gt(pred_segments, gt_segments):
    """
    For each predicted segment, find the best-matching ground truth segment by IoU over line sets.
    IoU is weighted by predicted segment size / total predicted lines.

    :return: a float in [0, 1] representing the weighted match quality from prediction to ground truth.
    """
    if not gt_segments and not pred_segments:
        return 1.0
    if not gt_segments or not pred_segments:
        return 0.0
    
    pred_sets = _to_sets(pred_segments)
    gt_sets = _to_sets(gt_segments)
    total_pred = sum(len(s) for s in pred_sets)
    if total_pred == 0:
        total_pred = 1  # if no predictions, set to 1 to avoid div by zero

    score = 0.0
    for p in pred_sets:
        best = max((_iou(p, g) for g in gt_sets))
        score += best * (len(p) / total_pred)
    return score

def _gt2pred(pred_segments, gt_segments):
    """
    For each ground truth segment, find the best-matching predicted segment by IoU over line sets.
    IoU is weighted by ground truth segment size / total ground truth lines.

    :return: a float in [0, 1] representing the weighted match quality from ground truth to prediction.
    """
    if not gt_segments and not pred_segments:
        return 1.0
    if not gt_segments or not pred_segments:
        return 0.0
    
    pred_sets = _to_sets(pred_segments)
    gt_sets = _to_sets(gt_segments)
    total_gt = sum(len(s) for s in gt_sets)
    if total_gt == 0:
        total_gt = 1  # if no GT, set to 1 to avoid div by zero

    score = 0.0
    for g in gt_sets:
        best = max((_iou(g, p) for p in pred_sets))
        score += best * (len(g) / total_gt)
    return score

def segmentation_similarity(pred_segments, gt_segments):
    """
    Compute a segmentation similarity that penalizes over/under segmentation.

    :return: a float in [0, 1] representing the segmentation similarity. Higher is better.
    """
    p2g = _pred2gt(pred_segments, gt_segments)
    g2p = _gt2pred(pred_segments, gt_segments)
    return 0.5 * (p2g + g2p)

def segmentation_rate(pred_segments, gt_segments):
    """
    Compute normalized over and under segmentation rates.
    over = max(0, (|P|-|G|)/|G|)
    under = max(0, (|G|-|P|)/|G|)
    """
    P = len(pred_segments)
    G = len(gt_segments) or 1  # avoid div by zero
    over = max(0.0, (P - G) / G)
    under = max(0.0, (G - P) / G)
    return {"over_rate": over, "under_rate": under}

# ======== Boundary-Level Metrics ========
def boundary_score(pred_boundaries, gt_boundaries, k=0):
    """
    Compute boundary precision/recall/F1 with tolerance k.
    """
    if len(pred_boundaries) == 0 and len(gt_boundaries) == 0:
        return {"Precision": 1.0, "Recall": 1.0, "F1": 1.0}
    
    tp = _greedy_match(pred_boundaries, gt_boundaries, k)

    precision = tp / len(pred_boundaries) if pred_boundaries else 0.0
    recall = tp / len(gt_boundaries) if gt_boundaries else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {"Precision": precision, "Recall": recall, "F1": f1}

# ======== Generate Final Report ========
def generate_final_report(
        pred_segments, 
        gt_file, 
        tolerance=0, 
        score_weights={  # can change these weights to adjust the final score
        "seg_similarity": 0.6,
        "boundary_f1": 0.4,
        "over_penalty": 0.25,
        "under_penalty": 0.25,
    }):
    """
    Generate a final report combining all metrics.
    """
    gt_segments = _gt_segments(gt_file)

    seg_sim = segmentation_similarity(pred_segments, gt_segments)
    rate = segmentation_rate(pred_segments, gt_segments)  # {"over_rate": x, "under_rate": y}

    pred_b = _segments_to_boundaries(pred_segments)
    gt_b = _segments_to_boundaries(gt_segments)
    bnd_score = boundary_score(pred_b, gt_b, k=tolerance)     # {"Precision","Recall","F1"}

    positive = score_weights["seg_similarity"] * seg_sim + score_weights["boundary_f1"] * bnd_score["F1"]
    penalty = score_weights["over_penalty"] * rate["over_rate"] + score_weights["under_penalty"] * rate["under_rate"]
    composite = positive * max(0.0, 1.0 - penalty)
    composite = max(0.0, min(1.0, composite))

    report = {
        "counts": {
            "pred_segments": len(pred_segments),
            "gt_segments": len(gt_segments),
            "pred_boundaries": len(pred_b),
            "gt_boundaries": len(gt_b),
        },
        "group": {
            "similarity": seg_sim,
            "over_rate": rate["over_rate"],
            "under_rate": rate["under_rate"],
        },
        "boundary": {
            "tolerance": tolerance,
            "Precision": bnd_score["Precision"],
            "Recall": bnd_score["Recall"],
            "F1": bnd_score["F1"],
        },
        "weights": score_weights,
        "composite_score": composite,
    }
    return report
