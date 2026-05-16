DELETE FROM usuarios;

DELETE FROM mesa;

DELETE FROM reserva;

DELETE FROM reserva_mesa;

ALTER TABLE usuarios AUTO_INCREMENT = 1;
ALTER TABLE reserva AUTO_INCREMENT = 1;
ALTER TABLE mesa AUTO_INCREMENT = 1;

INSERT INTO usuarios (email, password, es_admin, reservas, canceladas) VALUES
('admin.lucas@restaurant.com', '$2b$12$K7q9...', TRUE, 0, 0),
('admin.sofia@restaurant.com', '$2b$12$M9w1...', TRUE, 0, 0),
('juan.perez@email.com', '$2b$12$ExAmPlE1...', FALSE, 3, 1),
('maria.gomez@email.com', '$2b$12$ExAmPlE2...', FALSE, 2, 0),
('diego.maradona@email.com', '$2b$12$ExAmPlE3...', FALSE, 5, 2),
('carla.rodriguez@email.com', '$2b$12$ExAmPlE4...', FALSE, 1, 0),
('luis.vazquez@email.com', '$2b$12$ExAmPlE5...', FALSE, 0, 0),
('ana.martinez@email.com', '$2b$12$ExAmPlE6...', FALSE, 4, 0),
('nico.gonzalez@email.com', '$2b$12$ExAmPlE7...', FALSE, 2, 1),
('flor.fernandez@email.com', '$2b$12$ExAmPlE8...', FALSE, 1, 0);

INSERT INTO mesa (numero, capacidad, interior, funcional) VALUES
(101, 2, TRUE, TRUE),  (102, 2, TRUE, TRUE),  (103, 4, TRUE, TRUE),  (104, 4, TRUE, TRUE),
(105, 4, TRUE, TRUE),  (106, 6, TRUE, TRUE),  (107, 6, TRUE, TRUE),  (108, 8, TRUE, TRUE),
(109, 2, TRUE, TRUE),  (110, 4, TRUE, TRUE),
(201, 2, FALSE, TRUE), (202, 2, FALSE, TRUE), (203, 4, FALSE, TRUE), (204, 4, FALSE, TRUE),
(205, 4, FALSE, TRUE), (206, 6, FALSE, TRUE), (207, 6, FALSE, TRUE), (208, 8, FALSE, TRUE),
(209, 2, FALSE, TRUE), (210, 4, FALSE, TRUE);

-- Using a recursive CTE to quickly generate 100 rows without writing them out manually
INSERT INTO reserva (id_usuario, interior, codigo_qr, comensales)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 100
)
SELECT 
    FLOOR(1 + (RAND() * 10)) AS id_usuario,          -- Random user ID between 1 and 10
    IF(RAND() > 0.5, TRUE, FALSE) AS interior,       -- Randomly indoor or outdoor preference
    MD5(RAND()) AS codigo_qr,                        -- Generates a mock unique QR hash string
    FLOOR(2 + (RAND() * 7)) AS comensales            -- Random party size between 2 and 6
FROM seq;


INSERT INTO reserva_mesa (id_reserva, id_mesa, estado, reseñada, hora_reserva, fecha)
WITH RECURSIVE seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 100
)
SELECT 
    n AS id_reserva,                                  -- Maps 1:1 with the 100 reservations we created
    FLOOR(1 + (RAND() * 20)) AS id_mesa,             -- Assigns one of the 20 tables randomly
    ELT(FLOOR(1 + (RAND() * 3)), 'pendiente', 'cancelada', 'finalizada') AS estado,
    IF(RAND() > 0.8, TRUE, FALSE) AS reseñada,
    -- Cycles times perfectly on the hour (18:00, 19:00, 20:00, 21:00, 22:00)
    CASE (n % 5)
        WHEN 0 THEN '18:00:00'
        WHEN 1 THEN '19:00:00'
        WHEN 2 THEN '20:00:00'
        WHEN 3 THEN '21:00:00'
        ELSE '22:00:00'
    END AS hora_reserva,
    -- Splits the 100 rows perfectly down the middle into 2 specific days
    IF(n <= 50, '2026-06-01', '2026-06-02') AS fecha
FROM seq;

UPDATE reserva_mesa SET reseñada = FALSE WHERE estado <> 'finalizada' --corrijo estado de reseñada