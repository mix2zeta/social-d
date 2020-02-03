CREATE TABLE file (
    name TEXT NOT NULL,
    hash TEXT,
    posted TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (hash)
);


CREATE TABLE data (
    id TEXT NOT NULL,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    time TIMESTAMP WITH TIME ZONE,
    engagement INTEGER check(engagement > 0),
    channel TEXT,
    owner_id TEXT,
    owner_name TEXT,
    PRIMARY KEY (id)
);