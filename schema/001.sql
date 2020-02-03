CREATE TABLE index (
    consumer_id TEXT NOT NULL,
    consumer_address TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (consumer_id)
);
