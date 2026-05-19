
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
    id_usuario,
    interior,
    fecha,
    codigo_qr,
    comensales
)
VALUES
(
    2,
    TRUE,
    DATE_SUB(NOW(), INTERVAL 10 DAY),
    'QR-RES-1001',
    2
),
(
    2,
    FALSE,
    DATE_SUB(NOW(), INTERVAL 5 DAY),
    'QR-RES-1002',
    4
),
(
    3,
    TRUE,
    DATE_SUB(NOW(), INTERVAL 2 DAY),
    'QR-RES-1003',
    2
),
(
    4,
    FALSE,
    DATE_SUB(NOW(), INTERVAL 15 DAY),
    'QR-RES-1004',
    6
);

-- reservas futuras
INSERT INTO reserva (
    id_usuario,
    interior,
    fecha,
    codigo_qr,
    comensales
)
VALUES
(
    2,
    TRUE,
    DATE_ADD(NOW(), INTERVAL 5 DAY),
    'QR-RES-2001',
    2
),
(
    3,
    FALSE,
    DATE_ADD(NOW(), INTERVAL 8 DAY),
    'QR-RES-2002',
    4
);

-- =========================
-- RELACION RESERVA / MESA
-- =========================

INSERT INTO reserva_mesa (
    id_reserva,
    id_mesa,
    estado,
    reseñada,
    hora_reserva,
    fecha
)
VALUES
(
    1,
    1,
    'finalizada',
    TRUE,
    DATE_SUB(NOW(), INTERVAL 10 DAY),
    DATE_SUB(NOW(), INTERVAL 10 DAY)
),
(
    2,
    3,
    'finalizada',
    FALSE,
    DATE_SUB(NOW(), INTERVAL 5 DAY),
    DATE_SUB(NOW(), INTERVAL 5 DAY)
),
(
    3,
    2,
    'finalizada',
    FALSE,
    DATE_SUB(NOW(), INTERVAL 2 DAY),
    DATE_SUB(NOW(), INTERVAL 2 DAY)
),
(
    4,
    4,
    'cancelada',
    FALSE,
    DATE_SUB(NOW(), INTERVAL 15 DAY),
    DATE_SUB(NOW(), INTERVAL 15 DAY)
),
(
    5,
    1,
    'pendiente',
    FALSE,
    DATE_ADD(NOW(), INTERVAL 5 DAY),
    DATE_ADD(NOW(), INTERVAL 5 DAY)
),
(
    6,
    3,
    'pendiente',
    FALSE,
    DATE_ADD(NOW(), INTERVAL 8 DAY),
    DATE_ADD(NOW(), INTERVAL 8 DAY)
);

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

-- =========================
-- EXTRA:
-- reserva múltiple mesas
-- =========================

INSERT INTO reserva_mesa (
    id_reserva,
    id_mesa,
    estado,
    reseñada,
    hora_reserva,
    fecha
)
VALUES
(
    3,
    1,
    'finalizada',
    FALSE,
    DATE_SUB(NOW(), INTERVAL 2 DAY),
    DATE_SUB(NOW(), INTERVAL 2 DAY)
);