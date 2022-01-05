DROP TABLE IF EXISTS partner;

CREATE TABLE partner(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_id CHAR(10) UNIQUE NOT NULL,
    trading_name VARCHAR(60) NOT NULL,
    owner_name VARCHAR(50) NOT NULL,
    document VARCHAR(25) UNIQUE NOT NULL,
    coverage_area TEXT NOT NULL,
    address TEXT NOT NULL
)