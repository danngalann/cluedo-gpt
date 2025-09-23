from enum import Enum

from tortoise import fields, models


class GameStatus(str, Enum):
    DEFINITION = "definition"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    EXPIRED = "expired"


class ConversationRole(str, Enum):
    # For definition-time conversation history (and tool calls)
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"  # AI reply
    TOOL = "tool"  # tool-result messages


class QAStatus(str, Enum):
    ASKED = "asked"
    ANSWERED = "answered"


class Player(models.Model):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=255, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "players"

    def __str__(self) -> str:
        return f"{self.name}"


class Game(models.Model):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=255, index=True)
    owner = fields.ForeignKeyField(
        "models.Player",
        related_name="owned_games",
        on_delete=fields.RESTRICT,
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    # Game configuration
    language = fields.CharField(max_length=30, default="english")
    locale = fields.CharField(max_length=30, default="us")
    max_questions = fields.IntField(default=None, null=True)
    max_proposals = fields.IntField(default=3, null=True)
    expiry_date = fields.DatetimeField(index=True)

    # Ground-truth solution (hidden from players)
    culprit = fields.CharField(max_length=255)
    weapon = fields.CharField(max_length=255)
    motive = fields.CharField(max_length=255)
    story = fields.TextField()

    status = fields.CharEnumField(GameStatus, default=GameStatus.DEFINITION)

    # Players participating in this game
    players = fields.ManyToManyField(
        "models.Player",
        related_name="games",
        through="game_players",
    )

    # One game -> one definition conversation
    # (Reverse relation via GameDefinitionConversation.game)
    definition_conversation: fields.ReverseRelation["GameDefinitionConversation"]

    class Meta:
        table = "games"
        indexes = (("status", "expiry_date"),)

    def __str__(self) -> str:
        return f"{self.name}"


class GameDefinitionConversation(models.Model):
    """
    Single definition-time conversation per Game.
    """

    id = fields.UUIDField(primary_key=True)
    game = fields.OneToOneField(
        "models.Game",
        related_name="definition_conversation",
        on_delete=fields.CASCADE,
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    # Reverse: messages
    messages: fields.ReverseRelation["DefinitionMessage"]

    class Meta:
        table = "game_definition_conversations"

    def __str__(self) -> str:
        return f"DefinitionConversation<{self.id}>"


class DefinitionMessage(models.Model):
    """
    Ordered conversation messages used to define the game.
    Includes USER/ASSISTANT/SYSTEM and TOOL messages.
    Order is enforced by (conversation_id, idx) unique constraint.
    """

    id = fields.UUIDField(primary_key=True)
    conversation = fields.ForeignKeyField(
        "models.GameDefinitionConversation",
        related_name="messages",
        on_delete=fields.CASCADE,
    )
    role = fields.CharEnumField(ConversationRole)
    # For USER/ASSISTANT/SYSTEM: the text to feed the model
    # For TOOL: usually the tool's output or a compact representation
    content = fields.TextField(null=True)

    # Deterministic ordering within a conversation.
    # Assign sequentially in application code (transactional).
    idx = fields.IntField()

    # Tool-specific fields (present when role == TOOL)
    tool_name = fields.CharField(max_length=100, null=True)
    tool_args = fields.JSONField(null=True)  # JSONB in Postgres
    tool_result = fields.JSONField(null=True)  # JSONB in Postgres
    tool_call_id = fields.CharField(max_length=100, null=True)  # for model APIs
    tool_latency_ms = fields.IntField(null=True)
    tool_error = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "definition_messages"
        unique_together = (("conversation_id", "idx"),)
        indexes = (
            ("conversation_id", "idx"),
            ("role",),
        )

    def __str__(self) -> str:
        return f"[{self.role}] {self.content[:60] if self.content else '<tool>'}"


class GameQuestion(models.Model):
    """
    Isolated question-answer pair for gameplay.
    Related to a specific game and player.
    """

    id = fields.UUIDField(primary_key=True)
    game = fields.ForeignKeyField(
        "models.Game",
        related_name="questions",
        on_delete=fields.CASCADE,
        index=True,
    )
    player = fields.ForeignKeyField(
        "models.Player",
        related_name="questions",
        on_delete=fields.CASCADE,
        index=True,
    )

    question_text = fields.TextField()
    answer_text = fields.TextField(null=True)

    status = fields.CharEnumField(QAStatus, default=QAStatus.ASKED)
    asked_at = fields.DatetimeField(auto_now_add=True)
    answered_at = fields.DatetimeField(null=True)

    class Meta:
        table = "game_questions"
        indexes = (
            ("game_id", "player_id", "asked_at"),
            ("game_id", "asked_at"),
        )


class Proposal(models.Model):
    """
    A player's solution attempt in a game.
    """

    id = fields.UUIDField(primary_key=True)
    game = fields.ForeignKeyField(
        "models.Game",
        related_name="proposals",
        on_delete=fields.CASCADE,
        index=True,
    )
    player = fields.ForeignKeyField(
        "models.Player",
        related_name="proposals",
        on_delete=fields.CASCADE,
        index=True,
    )

    culprit = fields.CharField(max_length=255)
    weapon = fields.CharField(max_length=255)
    motive = fields.CharField(max_length=255)

    # Grading snapshot at the time of submission
    correct_count = fields.IntField(null=True)  # 0..3
    is_culprit_correct = fields.BooleanField(null=True)
    is_weapon_correct = fields.BooleanField(null=True)
    is_motive_correct = fields.BooleanField(null=True)

    # Optional explanation from the AI
    explanation = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "proposals"
        indexes = (
            ("game_id", "player_id", "created_at"),
            ("player_id", "created_at"),
        )
