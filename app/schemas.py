from pydantic import BaseModel


class CodeRequest(BaseModel):
    code: str

class SoftwareMetrics(BaseModel):

    LOC_BLANK: float
    BRANCH_COUNT: float
    LOC_CODE_AND_COMMENT: float
    LOC_COMMENTS: float
    CYCLOMATIC_COMPLEXITY: float
    DESIGN_COMPLEXITY: float
    ESSENTIAL_COMPLEXITY: float
    LOC_EXECUTABLE: float
    HALSTEAD_CONTENT: float
    HALSTEAD_DIFFICULTY: float
    HALSTEAD_EFFORT: float
    HALSTEAD_ERROR_EST: float
    HALSTEAD_LENGTH: float
    HALSTEAD_LEVEL: float
    HALSTEAD_PROG_TIME: float
    HALSTEAD_VOLUME: float
    NUM_OPERANDS: float
    NUM_OPERATORS: float
    NUM_UNIQUE_OPERANDS: float
    NUM_UNIQUE_OPERATORS: float
    LOC_TOTAL: float