-- MYSQL version handle inserting data and have duplicate

INSERT IGNORE INTO employees (id, name, position, salary) VALUES
    (2, 'Bob', 'Developer', 80000),  -- Ignored because id = 2 already exists
    (4, 'David', 'Analyst', 70000);  -- Inserted successfully


INSERT INTO employees (id, name, position, salary) VALUES
    (2, 'Bob', 'Senior Developer', 85000),  -- Updates existing row with id = 2
    (4, 'David', 'Analyst', 70000)          -- Inserted successfully
ON DUPLICATE KEY UPDATE
    position = VALUES(position),  -- Updates the 'position' column for id = 2
    salary = VALUES(salary);      -- Updates the 'salary' column for id = 2


INSERT INTO store_visits (store_id, store_name, visits) VALUES
    (1, 'Store A', 5),        -- Increment visits by 5 for store_id = 1
    (3, 'Store C', 3)         -- Insert new row for store_id = 3
ON DUPLICATE KEY UPDATE
    visits = visits + VALUES(visits);  -- Adds 5 to current visits for store_id = 1



-- POSTGRES version handle inserting data and have duplicate

INSERT INTO employees (id, name, position, salary) VALUES
    (2, 'Bob', 'Developer', 80000),  -- Ignored because id = 2 already exists
    (4, 'David', 'Analyst', 70000)   -- Inserted successfully
ON CONFLICT (id) DO NOTHING;



INSERT INTO employees (id, name, position, salary) VALUES
    (2, 'Bob', 'Senior Developer', 85000),  -- Updates existing row with id = 2
    (4, 'David', 'Analyst', 70000)          -- Inserted successfully
ON CONFLICT (id) DO UPDATE
SET position = EXCLUDED.position,
    salary = EXCLUDED.salary;


INSERT INTO store_visits (store_id, store_name, visits) VALUES
    (1, 'Store A', 5),        -- Increment visits by 5 for store_id = 1
    (3, 'Store C', 3)         -- Insert new row for store_id = 3
ON CONFLICT (store_id) DO UPDATE
SET visits = store_visits.visits + EXCLUDED.visits;  -- Adds 5 to current visits for store_id = 1
