DELETE FROM reseña;
DELETE FROM reserva_mesa;
DELETE FROM reserva;

DELETE FROM mesa;
DELETE FROM servicios_extra;
DELETE FROM plato;
DELETE FROM categoria_plato;
DELETE FROM configuracion;

DELETE FROM usuarios;

ALTER TABLE usuarios AUTO_INCREMENT = 1;
ALTER TABLE categoria_plato AUTO_INCREMENT = 1;
ALTER TABLE plato AUTO_INCREMENT = 1;
ALTER TABLE reserva AUTO_INCREMENT = 1;
ALTER TABLE servicios_extra AUTO_INCREMENT = 1;
ALTER TABLE mesa AUTO_INCREMENT = 1;
ALTER TABLE reseña AUTO_INCREMENT = 1;

INSERT INTO categoria_plato (categoria)
VALUES
('Entrada'),
('Principal'),
('Postre'),
('Bebida');

INSERT INTO mesa (numero, capacidad, interior, funcional) VALUES
(101, 2, TRUE, TRUE),  (102, 2, TRUE, TRUE),  (103, 4, TRUE, TRUE),  (104, 4, TRUE, TRUE),
(105, 4, TRUE, TRUE),  (106, 6, TRUE, TRUE),  (107, 6, TRUE, TRUE),  (108, 8, TRUE, TRUE),
(109, 2, TRUE, TRUE),  (110, 4, TRUE, TRUE),
(201, 2, FALSE, TRUE), (202, 2, FALSE, TRUE), (203, 4, FALSE, TRUE), (204, 4, FALSE, TRUE),
(205, 4, FALSE, TRUE), (206, 6, FALSE, TRUE), (207, 6, FALSE, TRUE), (208, 8, FALSE, TRUE),
(209, 2, FALSE, TRUE), (210, 4, FALSE, TRUE);

INSERT INTO usuarios (
    email,
    password,
    es_admin
)
VALUES
    ('admin@puertohermoso.com',
    'scrypt:32768:8:1$AQdBA7UUcfyCWWpn$6495b90ec151405cde68f8d6bdc97ebf00643fb8e905ca583e861b5d83537efa362cec9dc3191fda54584a80d8b9cdf0e96a71144102e930a986ceb5d087575e',
    TRUE),
('u1@test.com', 'hash', FALSE),
('u2@test.com', 'hash', FALSE),
('u3@test.com', 'hash', FALSE),
('u4@test.com', 'hash', FALSE),
('u5@test.com', 'hash', FALSE),
('u6@test.com', 'hash', FALSE),
('u7@test.com', 'hash', FALSE),
('u8@test.com', 'hash', FALSE),
('u9@test.com', 'hash', FALSE),
('u10@test.com', 'hash', FALSE);


INSERT INTO reserva (id_reserva, id_usuario, estado_reserva, reseñada, hora_reserva, fecha, interior, uuid_qr, estado_qr, qr_expiracion, comensales) VALUES
(1, 1, 'pendiente', FALSE, '12:00:00', '2026-05-21', TRUE, '00000000-0000-0000-0000-000000000001', 'pendiente', '2026-05-21 14:00:00', 2),
(2, 2, 'pendiente', FALSE, '12:00:00', '2026-05-21', TRUE, '00000000-0000-0000-0000-000000000002', 'pendiente', '2026-05-21 14:00:00', 4),
(3, 3, 'pendiente', FALSE, '13:00:00', '2026-05-21', FALSE, '00000000-0000-0000-0000-000000000003', 'pendiente', '2026-05-21 15:00:00', 2),
(4, 4, 'pendiente', FALSE, '13:00:00', '2026-05-21', TRUE, '00000000-0000-0000-0000-000000000004', 'pendiente', '2026-05-21 15:00:00', 5),
(5, 5, 'pendiente', FALSE, '14:00:00', '2026-05-21', FALSE, '00000000-0000-0000-0000-000000000005', 'pendiente', '2026-05-21 16:00:00', 3),
(6, 6, 'pendiente', FALSE, '20:00:00', '2026-05-21', TRUE, '00000000-0000-0000-0000-000000000006', 'pendiente', '2026-05-21 22:00:00', 2),
(7, 7, 'pendiente', FALSE, '20:00:00', '2026-05-21', TRUE, '00000000-0000-0000-0000-000000000007', 'pendiente', '2026-05-21 22:00:00', 4),
(8, 8, 'pendiente', FALSE, '21:00:00', '2026-05-21', FALSE, '00000000-0000-0000-0000-000000000008', 'pendiente', '2026-05-21 23:00:00', 6),
(9, 9, 'pendiente', FALSE, '21:00:00', '2026-05-21', TRUE, '00000000-0000-0000-0000-000000000009', 'pendiente', '2026-05-21 23:00:00', 2),
(10, 10, 'pendiente', FALSE, '22:00:00', '2026-05-21', FALSE, '00000000-0000-0000-0000-000000000010', 'pendiente', '2026-05-22 00:00:00', 4),
(11, 11, 'pendiente', FALSE, '12:00:00', '2026-05-22', TRUE, '00000000-0000-0000-0000-000000000011', 'pendiente', '2026-05-22 14:00:00', 2),
(12, 1, 'pendiente', FALSE, '12:00:00', '2026-05-22', FALSE, '00000000-0000-0000-0000-000000000012', 'pendiente', '2026-05-22 14:00:00', 3),
(13, 2, 'pendiente', FALSE, '13:00:00', '2026-05-22', TRUE, '00000000-0000-0000-0000-000000000013', 'pendiente', '2026-05-22 15:00:00', 4),
(14, 3, 'pendiente', FALSE, '13:00:00', '2026-05-22', TRUE, '00000000-0000-0000-0000-000000000014', 'pendiente', '2026-05-22 15:00:00', 2),
(15, 4, 'pendiente', FALSE, '14:00:00', '2026-05-22', FALSE, '00000000-0000-0000-0000-000000000015', 'pendiente', '2026-05-22 16:00:00', 5),
(16, 5, 'pendiente', FALSE, '20:00:00', '2026-05-22', TRUE, '00000000-0000-0000-0000-000000000016', 'pendiente', '2026-05-22 22:00:00', 4),
(17, 6, 'pendiente', FALSE, '20:00:00', '2026-05-22', FALSE, '00000000-0000-0000-0000-000000000017', 'pendiente', '2026-05-22 22:00:00', 2),
(18, 7, 'pendiente', FALSE, '21:00:00', '2026-05-22', TRUE, '00000000-0000-0000-0000-000000000018', 'pendiente', '2026-05-22 23:00:00', 6),
(19, 8, 'pendiente', FALSE, '21:00:00', '2026-05-22', TRUE, '00000000-0000-0000-0000-000000000019', 'pendiente', '2026-05-22 23:00:00', 2),
(20, 9, 'pendiente', FALSE, '22:00:00', '2026-05-22', FALSE, '00000000-0000-0000-0000-000000000020', 'pendiente', '2026-05-23 00:00:00', 4),
(21, 10, 'pendiente', FALSE, '12:00:00', '2026-05-23', TRUE, '00000000-0000-0000-0000-000000000021', 'pendiente', '2026-05-23 14:00:00', 3),
(22, 11, 'pendiente', FALSE, '12:00:00', '2026-05-23', TRUE, '00000000-0000-0000-0000-000000000022', 'pendiente', '2026-05-23 14:00:00', 2),
(23, 1, 'pendiente', FALSE, '13:00:00', '2026-05-23', FALSE, '00000000-0000-0000-0000-000000000023', 'pendiente', '2026-05-23 15:00:00', 4),
(24, 2, 'pendiente', FALSE, '13:00:00', '2026-05-23', TRUE, '00000000-0000-0000-0000-000000000024', 'pendiente', '2026-05-23 15:00:00', 6),
(25, 3, 'pendiente', FALSE, '14:00:00', '2026-05-23', FALSE, '00000000-0000-0000-0000-000000000025', 'pendiente', '2026-05-23 16:00:00', 2),
(26, 4, 'pendiente', FALSE, '20:00:00', '2026-05-23', TRUE, '00000000-0000-0000-0000-000000000026', 'pendiente', '2026-05-23 22:00:00', 4),
(27, 5, 'pendiente', FALSE, '20:00:00', '2026-05-23', TRUE, '00000000-0000-0000-0000-000000000027', 'pendiente', '2026-05-23 22:00:00', 2),
(28, 6, 'pendiente', FALSE, '21:00:00', '2026-05-23', FALSE, '00000000-0000-0000-0000-000000000028', 'pendiente', '2026-05-23 23:00:00', 5),
(29, 7, 'pendiente', FALSE, '21:00:00', '2026-05-23', TRUE, '00000000-0000-0000-0000-000000000029', 'pendiente', '2026-05-23 23:00:00', 3),
(30, 8, 'pendiente', FALSE, '22:00:00', '2026-05-23', FALSE, '00000000-0000-0000-0000-000000000030', 'pendiente', '2026-05-24 00:00:00', 4),
(31, 9, 'pendiente', FALSE, '12:00:00', '2026-05-24', TRUE, '00000000-0000-0000-0000-000000000031', 'pendiente', '2026-05-24 14:00:00', 2),
(32, 10, 'pendiente', FALSE, '12:00:00', '2026-05-24', FALSE, '00000000-0000-0000-0000-000000000032', 'pendiente', '2026-05-24 14:00:00', 4),
(33, 11, 'pendiente', FALSE, '13:00:00', '2026-05-24', TRUE, '00000000-0000-0000-0000-000000000033', 'pendiente', '2026-05-24 15:00:00', 4),
(34, 1, 'pendiente', FALSE, '13:00:00', '2026-05-24', TRUE, '00000000-0000-0000-0000-000000000034', 'pendiente', '2026-05-24 15:00:00', 2),
(35, 2, 'pendiente', FALSE, '14:00:00', '2026-05-24', FALSE, '00000000-0000-0000-0000-000000000035', 'pendiente', '2026-05-24 16:00:00', 6),
(36, 3, 'pendiente', FALSE, '20:00:00', '2026-05-24', TRUE, '00000000-0000-0000-0000-000000000036', 'pendiente', '2026-05-24 22:00:00', 3),
(37, 4, 'pendiente', FALSE, '20:00:00', '2026-05-24', FALSE, '00000000-0000-0000-0000-000000000037', 'pendiente', '2026-05-24 22:00:00', 2),
(38, 5, 'pendiente', FALSE, '21:00:00', '2026-05-24', TRUE, '00000000-0000-0000-0000-000000000038', 'pendiente', '2026-05-24 23:00:00', 4),
(39, 6, 'pendiente', FALSE, '21:00:00', '2026-05-24', TRUE, '00000000-0000-0000-0000-000000000039', 'pendiente', '2026-05-24 23:00:00', 5),
(40, 7, 'pendiente', FALSE, '22:00:00', '2026-05-24', FALSE, '00000000-0000-0000-0000-000000000040', 'pendiente', '2026-05-25 00:00:00', 2),
(41, 8, 'pendiente', FALSE, '12:00:00', '2026-05-25', TRUE, '00000000-0000-0000-0000-000000000041', 'pendiente', '2026-05-25 14:00:00', 4),
(42, 9, 'pendiente', FALSE, '13:00:00', '2026-05-25', TRUE, '00000000-0000-0000-0000-000000000042', 'pendiente', '2026-05-25 15:00:00', 3),
(43, 10, 'pendiente', FALSE, '14:00:00', '2026-05-25', FALSE, '00000000-0000-0000-0000-000000000043', 'pendiente', '2026-05-25 16:00:00', 2),
(44, 11, 'pendiente', FALSE, '20:00:00', '2026-05-25', TRUE, '00000000-0000-0000-0000-000000000044', 'pendiente', '2026-05-25 22:00:00', 4),
(45, 1, 'pendiente', FALSE, '21:00:00', '2026-05-25', FALSE, '00000000-0000-0000-0000-000000000045', 'pendiente', '2026-05-25 23:00:00', 6),
(46, 2, 'pendiente', FALSE, '12:00:00', '2026-05-26', TRUE, '00000000-0000-0000-0000-000000000046', 'pendiente', '2026-05-26 14:00:00', 2),
(47, 3, 'pendiente', FALSE, '13:00:00', '2026-05-26', FALSE, '00000000-0000-0000-0000-000000000047', 'pendiente', '2026-05-26 15:00:00', 4),
(48, 4, 'pendiente', FALSE, '20:00:00', '2026-05-26', TRUE, '00000000-0000-0000-0000-000000000048', 'pendiente', '2026-05-26 22:00:00', 3),
(49, 5, 'pendiente', FALSE, '21:00:00', '2026-05-26', TRUE, '00000000-0000-0000-0000-000000000049', 'pendiente', '2026-05-26 23:00:00', 2),
(50, 6, 'pendiente', FALSE, '13:00:00', '2026-05-27', FALSE, '00000000-0000-0000-0000-000000000050', 'pendiente', '2026-05-27 15:00:00', 4);

INSERT INTO reserva_mesa (id_reserva, id_mesa) VALUES
(1, 1),  (2, 2),  (3, 3),  (4, 4),  (5, 5),
(6, 6),  (7, 7),  (8, 8),  (9, 9),  (10, 10),
(11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
(21, 1),  (22, 2),  (23, 3),  (24, 4),  (25, 5),
(26, 6),  (27, 7),  (28, 8),  (29, 9),  (30, 10),
(31, 11), (32, 12), (33, 13), (34, 14), (35, 15),
(36, 16), (37, 17), (38, 18), (39, 19), (40, 20),
(41, 5),  (42, 10), (43, 15), (44, 2),  (45, 18),
(46, 3),  (47, 8),  (48, 12), (49, 14), (50, 1);

INSERT INTO plato (
    id_categoria,
    nombre,
    link_imagen,
    precio,
    hay_stock,
    gluten,
    producto_animal,
    carnes,
    lactosa
)
VALUES
(
    1,
    'Bruschettas',
    'https://picsum.photos/500/300?1',
    8500,
    TRUE,
    TRUE,
    FALSE,
    FALSE,
    FALSE
),
(
    2,
    'Bife de chorizo',
    'https://picsum.photos/500/300?2',
    18500,
    TRUE,
    FALSE,
    TRUE,
    TRUE,
    FALSE
),
(
    2,
    'Risotto de hongos',
    'https://picsum.photos/500/300?3',
    14500,
    TRUE,
    TRUE,
    TRUE,
    FALSE,
    TRUE
),
(
    3,
    'Cheesecake',
    'https://picsum.photos/500/300?4',
    7500,
    TRUE,
    TRUE,
    TRUE,
    FALSE,
    TRUE
),
(
    4,
    'Limonada',
    'https://picsum.photos/500/300?5',
    4500,
    TRUE,
    FALSE,
    FALSE,
    FALSE,
    FALSE
);