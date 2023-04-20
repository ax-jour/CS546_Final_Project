DROP TABLE IF EXISTS users_thirdparty;

CREATE TABLE users_thirdparty (
    invitation_code TEXT PRIMARY KEY NOT NULL,
    fName TEXT,
    lName TEXT,
    dLicense TEXT,
    join_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -- Insert arbitrary users into the database during initialization.
-- INSERT INTO users_thirdparty (invitation_code)
-- VALUES (123456);

-- INSERT INTO users_thirdparty (invitation_code)
-- VALUES (654321);