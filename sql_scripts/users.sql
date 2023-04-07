DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id TEXT PRIMARY KEY NOT NULL,
    prover_key TEXT NOT NULL,
    verifier_key TEXT NOT NULL,
    join_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert arbitrary users into the database during initialization.
INSERT INTO users (user_id, prover_key, verifier_key)
VALUES ('user_account1', 'pk111', 'vk111');

INSERT INTO users (user_id, prover_key, verifier_key)
VALUES ('user_account2', '222', '222');