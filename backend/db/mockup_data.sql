DELETE FROM usuarios WHERE email != 'admin@puertohermoso.com';

DELETE FROM mesa;

DELETE FROM reserva;

DELETE FROM reserva_mesa;

DELETE FROM reseña;

DELETE FROM plato;

DELETE FROM servicios_extra;
ALTER TABLE usuarios AUTO_INCREMENT = 1;
ALTER TABLE reserva AUTO_INCREMENT = 1;
ALTER TABLE mesa AUTO_INCREMENT = 1;

ALTER TABLE plato AUTO_INCREMENT = 1;
ALTER TABLE reseña AUTO_INCREMENT = 1;
ALTER TABLE servicios_extra AUTO_INCREMENT = 1;


-- =========================
-- USUARIOS
-- =========================

INSERT INTO usuarios (
    email,
    password,
    es_admin,
    reservas,
    canceladas
)
VALUES
(
    'juan@gmail.com',
    '1234',
    FALSE,
    5,
    1
),
(
    'maria@gmail.com',
    '1234',
    FALSE,
    3,
    0
),
(
    'pedro@gmail.com',
    '1234',
    FALSE,
    2,
    2
),
(
    'lucia@gmail.com',
    '1234',
    FALSE,
    7,
    1
);

-- =========================
-- MESAS
-- =========================

INSERT INTO mesa (
    numero,
    capacidad,
    interior,
    funcional
)
VALUES
(1, 2, TRUE, TRUE),
(2, 4, TRUE, TRUE),
(3, 6, FALSE, TRUE),
(4, 8, FALSE, TRUE),
(5, 2, TRUE, FALSE);

-- =========================
-- SERVICIOS EXTRA
-- =========================

INSERT INTO servicios_extra (
    nombre,
    descripcion,
    disponible
)
VALUES
(
    'Decoracion romantica',
    'Velas y flores para ocasiones especiales',
    TRUE
),
(
    'Menu vegano',
    'Opciones 100% vegetales',
    TRUE
),
(
    'Show en vivo',
    'Musica en vivo viernes y sabados',
    FALSE
);

-- =========================
-- PLATOS
-- =========================

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

-- =========================
-- RESERVAS
-- =========================

-- reservas pasadas
INSERT INTO reserva (
    id_usuario
)
VALUES
(
    2
),
(
    2
),
(
    3
),
(
    4
);

-- reservas futuras
INSERT INTO reserva (
    id_usuario
)
VALUES
(
    2
),
(
    3
);

-- =========================
-- RELACION RESERVA / MESA
-- =========================

INSERT INTO reserva_mesa (
    id_reserva, 
    id_mesa, 
    estado_reserva, 
    pendiente_reseña, 
    hora_reserva, 
    fecha, 
    interior, 
    uuid_qr, 
    estado_qr, 
    qr_expiracion, 
    comensales
) VALUES
(1, 1, 'pendiente', FALSE, '12:00:00', '2026-05-21', TRUE,  '11111111-1111-1111-1111-111111111111', 'pendiente', '2026-05-21 14:00:00', 2),
(2, 2, 'pendiente', FALSE, '13:00:00', '2026-05-21', TRUE,  '22222222-2222-2222-2222-222222222222', 'pendiente', '2026-05-21 15:00:00', 4),
(3, 3, 'pendiente', FALSE, '20:00:00', '2026-05-22', FALSE, '33333333-3333-3333-3333-333333333333', 'pendiente', '2026-05-22 22:00:00', 2),
(4, 4, 'pendiente', FALSE, '21:00:00', '2026-05-22', TRUE,  '44444444-4444-4444-4444-444444444444', 'pendiente', '2026-05-22 23:00:00', 6),
(5, 1, 'pendiente', FALSE, '14:00:00', '2026-05-23', FALSE, '55555555-5555-5555-5555-555555555555', 'pendiente', '2026-05-23 16:00:00', 3),
(6, 2, 'pendiente', FALSE, '22:00:00', '2026-05-24', TRUE,  '66666666-6666-6666-6666-666666666666', 'pendiente', '2026-05-24 00:00:00', 4);

-- =========================
-- RESEÑAS
-- =========================

INSERT INTO reseña (
    id_usuario,
    id_reserva,
    calificacion,
    comentario,
    estado
)
VALUES
(
    2,
    1,
    5,
    'Excelente experiencia. La comida espectacular.',
    'aprobada'
),
(
    4,
    4,
    2,
    'Tardaron mucho en atendernos.',
    'no_aprobada'
),
(
    3,
    3,
    4,
    'Muy buen ambiente y buena comida.',
    'no_revisada'
);