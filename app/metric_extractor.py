from radon.metrics import h_visit
from radon.complexity import cc_visit
from radon.raw import analyze



def extract_metrics(code: str):

    # Halstead Metrics
    halstead = h_visit(code)

    # Cyclomatic Complexity
    complexity_results = cc_visit(code)

    avg_complexity = 0

    if complexity_results:
        avg_complexity = sum(
            obj.complexity
            for obj in complexity_results
        ) / len(complexity_results)

    metrics = {
        "HALSTEAD_LENGTH": halstead.total.length,
        "HALSTEAD_VOLUME": halstead.total.volume,
        "HALSTEAD_DIFFICULTY": halstead.total.difficulty,
        "HALSTEAD_EFFORT": halstead.total.effort,
        "HALSTEAD_PROG_TIME": halstead.total.time,
        "HALSTEAD_ERROR_EST": halstead.total.bugs,
        "CYCLOMATIC_COMPLEXITY": avg_complexity
    }

    return metrics


code = """
def divide(a,b):
    if b == 0:
        return -1
    return a/b
"""

raw_metrics = analyze(code)
print(extract_metrics(code))
print(raw_metrics)

"""
output:
{'HALSTEAD_LENGTH': 8, 
'HALSTEAD_VOLUME': 22.458839376460833, 
'HALSTEAD_DIFFICULTY': 1.875, 
'HALSTEAD_EFFORT': 42.11032383086406, 
'HALSTEAD_PROG_TIME': 2.3394624350480036, 
'HALSTEAD_ERROR_EST': 0.007486279792153611, 
'CYCLOMATIC_COMPLEXITY': 2.0}

Module(
loc=5, 
lloc=4, 
sloc=4, 
comments=0, 
multi=0, 
blank=1, 
single_comments=0
)
"""
