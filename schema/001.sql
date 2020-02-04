CREATE TABLE file (
    name TEXT NOT NULL,
    hash TEXT NOT NULL,
    split TEXT NOT NULL,
    task_id TEXT,
    posted TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (hash, split)
);


CREATE TABLE data (
    id TEXT NOT NULL,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    time TIMESTAMP WITH TIME ZONE,
    engagement INTEGER check(engagement >= 0),
    channel TEXT,
    owner_id TEXT,
    owner_name TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE data_error(
    data TEXT NOT NULL,
    from_file TEXT NOT NULL,
    posted TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE processed (
    date DATE NOT NULL,
    reverse_index JSON,
    word_count JSON,
    PRIMARY KEY (date)
);

