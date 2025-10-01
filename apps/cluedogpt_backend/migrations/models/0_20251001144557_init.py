from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "players" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_players_name_846625" ON "players" ("name");
CREATE TABLE IF NOT EXISTS "games" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "language" VARCHAR(30) NOT NULL DEFAULT 'english',
    "locale" VARCHAR(30) NOT NULL DEFAULT 'us',
    "max_questions" INT,
    "max_proposals" INT DEFAULT 3,
    "expiry_date" TIMESTAMPTZ NOT NULL,
    "culprit" VARCHAR(255) NOT NULL,
    "weapon" VARCHAR(255) NOT NULL,
    "motive" VARCHAR(255) NOT NULL,
    "story" TEXT NOT NULL,
    "status" VARCHAR(10) NOT NULL DEFAULT 'definition',
    "owner_id" UUID NOT NULL REFERENCES "players" ("id") ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS "idx_games_name_f50d57" ON "games" ("name");
CREATE INDEX IF NOT EXISTS "idx_games_expiry__915010" ON "games" ("expiry_date");
CREATE INDEX IF NOT EXISTS "idx_games_status_04bf4c" ON "games" ("status", "expiry_date");
COMMENT ON COLUMN "games"."status" IS 'DEFINITION: definition\nONGOING: ongoing\nCOMPLETED: completed\nEXPIRED: expired';
CREATE TABLE IF NOT EXISTS "game_definition_conversations" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "game_id" UUID NOT NULL UNIQUE REFERENCES "games" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "game_definition_conversations" IS 'Single definition-time conversation per Game.';
CREATE TABLE IF NOT EXISTS "definition_messages" (
    "id" UUID NOT NULL PRIMARY KEY,
    "role" VARCHAR(9) NOT NULL,
    "content" TEXT,
    "idx" INT NOT NULL,
    "tool_name" VARCHAR(100),
    "tool_args" JSONB,
    "tool_result" JSONB,
    "tool_call_id" VARCHAR(100),
    "tool_latency_ms" INT,
    "tool_error" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "conversation_id" UUID NOT NULL REFERENCES "game_definition_conversations" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_definition__convers_347056" UNIQUE ("conversation_id", "idx")
);
CREATE INDEX IF NOT EXISTS "idx_definition__convers_347056" ON "definition_messages" ("conversation_id", "idx");
CREATE INDEX IF NOT EXISTS "idx_definition__role_ca15d1" ON "definition_messages" ("role");
COMMENT ON COLUMN "definition_messages"."role" IS 'SYSTEM: system\nUSER: user\nASSISTANT: assistant\nTOOL: tool';
COMMENT ON TABLE "definition_messages" IS 'Ordered conversation messages used to define the game.';
CREATE TABLE IF NOT EXISTS "game_questions" (
    "id" UUID NOT NULL PRIMARY KEY,
    "question_text" TEXT NOT NULL,
    "answer_text" TEXT,
    "status" VARCHAR(8) NOT NULL DEFAULT 'asked',
    "asked_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "answered_at" TIMESTAMPTZ,
    "game_id" UUID NOT NULL REFERENCES "games" ("id") ON DELETE CASCADE,
    "player_id" UUID NOT NULL REFERENCES "players" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_game_questi_game_id_c41648" ON "game_questions" ("game_id");
CREATE INDEX IF NOT EXISTS "idx_game_questi_player__48498a" ON "game_questions" ("player_id");
CREATE INDEX IF NOT EXISTS "idx_game_questi_game_id_5f64e1" ON "game_questions" ("game_id", "player_id", "asked_at");
CREATE INDEX IF NOT EXISTS "idx_game_questi_game_id_7f7c67" ON "game_questions" ("game_id", "asked_at");
COMMENT ON COLUMN "game_questions"."status" IS 'ASKED: asked\nANSWERED: answered';
COMMENT ON TABLE "game_questions" IS 'Isolated question-answer pair for gameplay.';
CREATE TABLE IF NOT EXISTS "proposals" (
    "id" UUID NOT NULL PRIMARY KEY,
    "culprit" VARCHAR(255) NOT NULL,
    "weapon" VARCHAR(255) NOT NULL,
    "motive" VARCHAR(255) NOT NULL,
    "correct_count" INT,
    "is_culprit_correct" BOOL,
    "is_weapon_correct" BOOL,
    "is_motive_correct" BOOL,
    "explanation" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "game_id" UUID NOT NULL REFERENCES "games" ("id") ON DELETE CASCADE,
    "player_id" UUID NOT NULL REFERENCES "players" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_proposals_game_id_a49234" ON "proposals" ("game_id");
CREATE INDEX IF NOT EXISTS "idx_proposals_player__001ae3" ON "proposals" ("player_id");
CREATE INDEX IF NOT EXISTS "idx_proposals_game_id_f42bac" ON "proposals" ("game_id", "player_id", "created_at");
CREATE INDEX IF NOT EXISTS "idx_proposals_player__9ed3bb" ON "proposals" ("player_id", "created_at");
COMMENT ON TABLE "proposals" IS 'A player''s solution attempt in a game.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "game_players" (
    "games_id" UUID NOT NULL REFERENCES "games" ("id") ON DELETE CASCADE,
    "player_id" UUID NOT NULL REFERENCES "players" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_game_player_games_i_aa66f9" ON "game_players" ("games_id", "player_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
