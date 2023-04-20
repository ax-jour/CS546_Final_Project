DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
    vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_title TEXT NOT NULL,
    op1 TEXT NOT NULL,
    op1_ct INTEGER NOT NULL DEFAULT 0,
    op2 TEXT NOT NULL,
    op2_ct INTEGER NOT NULL DEFAULT 0,
    op3 TEXT NOT NULL,
    op3_ct INTEGER NOT NULL DEFAULT 0,
    vote_participants_ct INTEGER NOT NULL,
    vote_isComplete BOOLEAN NOT NULL DEFAULT FALSE
);

DROP TABLE IF EXISTS votes_participants;

CREATE TABLE votes_participants (
    vote_id INTEGER NOT NULL,
    participant TEXT NOT NULL
);

-- Insert arbitrary votes into the database during initialization.
INSERT INTO votes (vote_title, op1, op2, op3, vote_participants_ct)
VALUES ('First Default Vote Title', 'Selection A', 'Selection B', 'Selection C', 10);

INSERT INTO votes (vote_title, op1, op2, op3, vote_participants_ct)
VALUES ('Second Default Vote Title', 'Selection A', 'Selection B', 'Selection C', 20);