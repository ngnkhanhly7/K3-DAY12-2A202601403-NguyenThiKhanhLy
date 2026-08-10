"""Mock LLM used by the lab.

The function is deterministic: the same question returns the same style of
answer, so tests are stable and no real LLM API key is needed.
"""

from __future__ import annotations

import hashlib

PRICE_INPUT_PER_1K = 0.00015
PRICE_OUTPUT_PER_1K = 0.00060

_TEMPLATES = [
    "Theo mình hiểu, {q} liên quan tới cách hệ thống được đóng gói và vận hành. "
    "Điểm mấu chốt là tách cấu hình ra khỏi code và giữ service ở trạng thái stateless.",
    "Câu hỏi hay. {q} thường được giải quyết bằng cách chuẩn hóa môi trường chạy: "
    "cùng một image chạy giống nhau ở laptop và trên cloud.",
    "Ngắn gọn: {q} phụ thuộc vào ba yếu tố: cấu hình qua biến môi trường, "
    "health check để orchestrator biết trạng thái, và giới hạn tài nguyên.",
    "Với {q}, cách làm phổ biến trong production là đặt một lớp gateway phía trước "
    "để lo authentication, rate limiting và bảo vệ chi phí.",
]


def _estimate_tokens(text: str) -> int:
    """Rough estimate: about 4 characters per token, minimum 1."""
    return max(1, len(text) // 4)


def ask_llm(question: str, history: list[dict] | None = None) -> dict:
    """Simulate one LLM call."""
    history = history or []
    digest = hashlib.sha256(question.strip().lower().encode("utf-8")).hexdigest()
    template = _TEMPLATES[int(digest[:8], 16) % len(_TEMPLATES)]
    answer = template.format(q=question.strip().rstrip("?") or "vấn đề bạn hỏi")

    if history:
        answer += f" (Mình đang nhớ {len(history)} lượt trao đổi trước đó.)"

    prompt_text = question + "".join(turn.get("content", "") for turn in history)
    tokens_in = _estimate_tokens(prompt_text)
    tokens_out = _estimate_tokens(answer)
    cost = (
        tokens_in / 1000 * PRICE_INPUT_PER_1K
        + tokens_out / 1000 * PRICE_OUTPUT_PER_1K
    )

    return {
        "answer": answer,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round(cost, 8),
    }
