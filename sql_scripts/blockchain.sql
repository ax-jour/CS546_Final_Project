DROP TABLE IF EXISTS blockchain;   

CREATE TABLE blockchain (
    idx INTEGER PRIMARY KEY,
    ts TEXT,
    proof TEXT,
    previous_hash TEXT,
    data_pk TEXT,
    data_hs TEXT,
    data_vote TEXT
);