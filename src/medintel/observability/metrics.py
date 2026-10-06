from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "medintel_requests_total",
    "Total number of application requests.",
)

REQUEST_ERRORS = Counter(
    "medintel_request_errors_total",
    "Total number of failed application requests.",
)

RETRIEVAL_LATENCY = Histogram(
    "medintel_retrieval_latency_seconds",
    "Time spent retrieving evidence.",
)

LLM_LATENCY = Histogram(
    "medintel_llm_latency_seconds",
    "Time spent generating an LLM response.",
)

LLM_INPUT_TOKENS = Counter(
    "medintel_llm_input_tokens_total",
    "Total number of LLM input tokens.",
)

LLM_OUTPUT_TOKENS = Counter(
    "medintel_llm_output_tokens_total",
    "Total number of LLM output tokens.",
)

LLM_COST = Counter(
    "medintel_llm_cost_usd_total",
    "Estimated total LLM generation cost in USD.",
)

RETRIEVED_CHUNKS = Histogram(
    "medintel_retrieved_chunks",
    "Number of chunks retrieved per request.",
)