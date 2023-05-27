CREATE TABLE IF NOT EXISTS lwtdemo.script_records (
id SERIAL PRIMARY KEY,
title CHAR(100),
date_info CHAR(100),
sentiment JSONB,
sentence TEXT,
sadness_score decimal ,
joy_score decimal,
love_score decimal,
anger_score decimal,
fear_score decimal,
surprise_score decimal
);

