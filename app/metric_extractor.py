from radon.metrics import h_visit
from radon.complexity import cc_visit
from radon.raw import analyze


def extract_metrics(code: str):

    halstead = h_visit(code)
    raw = analyze(code)
    complexity = cc_visit(code)

    avg_cc = 0

    if complexity:
        avg_cc = sum(
            item.complexity
            for item in complexity
        ) / len(complexity)

    return {
        "LOC_TOTAL": raw.loc,
        "LOC_EXECUTABLE": raw.sloc,
        "LOC_BLANK": raw.blank,
        "LOC_COMMENTS": raw.comments,

        "CYCLOMATIC_COMPLEXITY": avg_cc,

        "HALSTEAD_LENGTH": halstead.total.length,
        "HALSTEAD_VOLUME": halstead.total.volume,
        "HALSTEAD_DIFFICULTY": halstead.total.difficulty,
        "HALSTEAD_EFFORT": halstead.total.effort,
        "HALSTEAD_PROG_TIME": halstead.total.time,
        "HALSTEAD_ERROR_EST": halstead.total.bugs,
    }

def add_engineered_features(metrics):

    metrics["COMPLEXITY_DENSITY"] = (
        metrics["CYCLOMATIC_COMPLEXITY"]
        / (metrics["LOC_TOTAL"] + 1)
    )

    metrics["COMMENT_RATIO"] = (
        metrics["LOC_COMMENTS"]
        / (metrics["LOC_TOTAL"] + 1)
    )

    return metrics