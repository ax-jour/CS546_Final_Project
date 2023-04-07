DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
    vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_title TEXT NOT NULL,
    op1 TEXT NOT NULL,
    op1_ct INTEGER NOT NULL DEFAULT 0,
    op2 TEXT NOT NULL,
    op2_ct INTEGER NOT NULL DEFAULT 0,
    vote_participants_ct INTEGER NOT NULL,
    vote_isComplete BOOLEAN NOT NULL DEFAULT FALSE
);

-- Insert arbitrary votes into the database during initialization.
INSERT INTO votes (vote_title, op1, op2, vote_participants_ct)
VALUES ('First Default 2 choices Vote Title', 'Selection A', 'Selection B', 10);

INSERT INTO votes (vote_title, op1, op2, vote_participants_ct)
VALUES ('Second Default 4 choices Vote Title', 'Selection A', 'Selection B', 20);