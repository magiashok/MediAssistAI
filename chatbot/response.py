import re

from chatbot.groq_client import client
from chatbot.prompts import SYSTEM_PROMPT

# Phrases suggesting the user may be in a mental health crisis (suicidal ideation
# or self-harm intent). Kept deliberately narrow to strong, unambiguous signals —
# broad words like "sad" or "stressed" are NOT included, to avoid false positives
# on ordinary wellness questions this bot is meant to answer.
CRISIS_PATTERNS = [
    r"\bkill(ing)?\s+myself\b",
    r"\bend(ing)?\s+my\s+life\b",
    r"\bsuicid(e|al)\b",
    r"\bwant(ed)?\s+to\s+die\b",
    r"\bdon'?t\s+want\s+to\s+(be\s+alive|live)\b",
    r"\bself[\s-]?harm\b",
    r"\bhurt(ing)?\s+myself\b",
    r"\bno\s+reason\s+to\s+live\b",
    r"\bbetter\s+off\s+dead\b",
    r"\bending\s+it\s+all\b",
]
CRISIS_REGEX = re.compile("|".join(CRISIS_PATTERNS), re.IGNORECASE)

# India-based helplines, verified August 2026 — worth periodically re-checking,
# as helpline numbers do change over time.
CRISIS_RESPONSE = (
    "💙 It sounds like you might be going through something really difficult right now. "
    "I'm not able to provide crisis support, but please don't go through this alone — "
    "free, confidential help is available:\n\n"
    "- **KIRAN Mental Health Helpline (Govt. of India):** 1800-599-0019 (24/7, toll-free)\n"
    "- **Vandrevala Foundation:** 1860-266-2345 or 9999-666-555 (24/7)\n\n"
    "If you're in immediate danger, please contact your local emergency services or go to "
    "the nearest hospital right away. You matter, and there are people who want to help."
)


def is_crisis_message(text):
    return bool(CRISIS_REGEX.search(text or ""))

try:
    from groq import (
        RateLimitError,
        AuthenticationError,
        APIConnectionError,
        APITimeoutError,
        APIStatusError,
    )
except ImportError:
    # Older/newer groq SDK versions may not expose all of these names.
    # Fall back to broad Exception handling below if so.
    RateLimitError = AuthenticationError = APIConnectionError = APITimeoutError = APIStatusError = Exception

# Friendly, non-technical messages shown to users when something goes wrong.
# Keeping these separate from the raw error means a public user never sees
# a stack trace or API-specific jargon.
FRIENDLY_ERRORS = {
    "rate_limit": (
        "🙏 I'm getting a lot of questions right now and have hit my usage limit "
        "for the moment. Please try again in a few minutes."
    ),
    "auth": (
        "⚠️ There's a configuration issue on my end (the service key needs attention). "
        "Please let the site admin know — this isn't something you can fix on your side."
    ),
    "connection": (
        "🔌 I'm having trouble connecting to the AI service right now. "
        "Please check your connection and try again in a moment."
    ),
    "generic": (
        "😕 Something went wrong while I was working on your answer. "
        "Please try asking again — if this keeps happening, let the site admin know."
    ),
}


# How many recent messages (user + assistant combined) to send to the API
# per turn. 10 messages ≈ 5 back-and-forth exchanges — enough for the model
# to keep conversational context without cost/rate-limit growing unbounded.
MAX_HISTORY_MESSAGES = 10


def get_ai_response(messages):
    # Check the latest user message for crisis language before doing anything
    # else — this runs locally, with no API call, so it still works even if
    # the AI service is down or the key has run out. That reliability matters
    # more here than anywhere else in the app.
    last_user_message = next(
        (m["content"] for m in reversed(messages) if m.get("role") == "user"), ""
    )
    if is_crisis_message(last_user_message):
        return CRISIS_RESPONSE

    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Only send the most recent messages to the API. The full history still
    # displays on screen (that's tracked separately in session state) — this
    # just controls what gets *sent* each turn, so token usage (and therefore
    # cost and how fast the rate limit gets hit) doesn't grow unbounded as a
    # conversation gets long.
    conversation.extend(messages[-MAX_HISTORY_MESSAGES:])

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content

    except RateLimitError:
        return FRIENDLY_ERRORS["rate_limit"]
    except AuthenticationError:
        return FRIENDLY_ERRORS["auth"]
    except (APIConnectionError, APITimeoutError):
        return FRIENDLY_ERRORS["connection"]
    except APIStatusError as e:
        # Catch-all for other API-side errors (e.g. 4xx/5xx we didn't name above).
        # A 429 status sometimes surfaces here depending on SDK version, so check it explicitly.
        if getattr(e, "status_code", None) == 429:
            return FRIENDLY_ERRORS["rate_limit"]
        return FRIENDLY_ERRORS["generic"]
    except Exception:
        # Last-resort safety net so the app never crashes with a raw traceback
        # in front of a public user.
        return FRIENDLY_ERRORS["generic"]