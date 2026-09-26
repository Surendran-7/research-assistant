"""
The core agent: runs a Groq tool-calling loop, letting the model decide when
to search the uploaded documents, the web, or Wikipedia, then produces a
grounded, cited answer.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List

from groq import Groq

from config.settings import settings
from prompts.research_prompt import RESEARCH_SYSTEM_PROMPT
from tools.document_tool import TOOL_SCHEMA as DOC_TOOL, search_documents
from tools.web_search import TOOL_SCHEMA as WEB_TOOL, web_search
from tools.wikipedia_tool import TOOL_SCHEMA as WIKI_TOOL, wikipedia_search

TOOLS = [DOC_TOOL, WEB_TOOL, WIKI_TOOL]

TOOL_FUNCTIONS = {
    "search_documents": search_documents,
    "web_search": web_search,
    "wikipedia_search": wikipedia_search,
}


@dataclass
class ResearchResult:
    answer: str
    tool_calls_made: List[str] = field(default_factory=list)


class ResearchAgent:
    def __init__(self, model: str = settings.GROQ_MODEL, max_tool_rounds: int = 5):
        settings.validate()
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = model
        self.max_tool_rounds = max_tool_rounds

    def run(self, question: str) -> ResearchResult:
        messages = [
            {"role": "system", "content": RESEARCH_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
        tool_log: List[str] = []

        for _ in range(self.max_tool_rounds):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.2,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                return ResearchResult(answer=message.content or "", tool_calls_made=tool_log)

            # The model wants to call one or more tools — execute them and feed results back.
            messages.append(message.model_dump(exclude_unset=True))
            for call in message.tool_calls:
                fn_name = call.function.name
                args = json.loads(call.function.arguments or "{}")
                tool_log.append(f"{fn_name}({args})")

                fn = TOOL_FUNCTIONS.get(fn_name)
                result = fn(**args) if fn else f"Unknown tool: {fn_name}"

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": fn_name,
                        "content": result,
                    }
                )

        # Ran out of tool rounds — force a final answer with no more tool access.
        final = self.client.chat.completions.create(
            model=self.model,
            messages=messages + [{"role": "user", "content": "Give your best final answer now."}],
            temperature=0.2,
        )
        return ResearchResult(answer=final.choices[0].message.content or "", tool_calls_made=tool_log)
