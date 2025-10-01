from dataclasses import dataclass


@dataclass
class AgentDepedencies:
    conversation_id: str
    user_id: int
