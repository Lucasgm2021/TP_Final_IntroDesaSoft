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

INSERT INTO configuracion (clave, valor)
VALUES
(
    'nombre_restaurante',
    'PUERTO HERMOSO'
),
(
    'telefono',
    '+54 11 1234-5678'
),
(
    'horario',
    'Lunes a Domingo 12:00 - 00:00'
),
(
    'historia',
    'Puerto Hermoso nació en 1974, cuando las calles de Palermo Soho todavía conservaban su ritmo de barrio y talleres. Lo que comenzó como un pequeño sueño familiar de mesas compartidas y sabores honestos, se transformó en un punto de encuentro que ha atravesado décadas.
Hoy, tres generaciones después, mantenemos intacta la esencia que nos dio origen: la calidez del trato familiar y el respeto por la cocina bien hecha. Somos la historia viva de un barrio que amamos, evolucionando con el tiempo pero conservando siempre el corazón en nuestros fuegos.
Medio siglo de familia, encuentros y pasión por la mesa.'
);

INSERT INTO usuarios (
    email,
    password,
    es_admin,
    reservas,
    canceladas
)
VALUES
(
    'admin@puertohermoso.com',
    '1234',
    TRUE,
    0,
    0
),
(
    'juan.perez@email.com',
    '1234',
    FALSE,
    3,
    1
),
(
    'maria.gomez@email.com',
    '1234',
    FALSE,
    5,
    0
),
(
    'diego.maradona@email.com',
    '1234',
    FALSE,
    2,
    1
),
(
    'carla.rodriguez@email.com',
    '1234',
    FALSE,
    1,
    0
),
(
    'luis.vazquez@email.com',
    '1234',
    FALSE,
    4,
    2
),
(
    'ana.martinez@email.com',
    '1234',
    FALSE,
    2,
    0
);

INSERT INTO mesa (
    numero,
    capacidad,
    interior,
    funcional
)
VALUES
(101, 2, TRUE, TRUE),
(102, 2, TRUE, TRUE),
(103, 4, TRUE, TRUE),
(104, 4, TRUE, TRUE),
(105, 6, TRUE, TRUE),
(201, 2, FALSE, TRUE),
(202, 4, FALSE, TRUE),
(203, 6, FALSE, TRUE),
(204, 8, FALSE, TRUE),
(205, 4, FALSE, FALSE);

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

INSERT INTO reserva (
    id_usuario,
    estado_reserva,
    reseñada,
    hora_reserva,
    fecha,
    interior,
    uuid_qr,
    estado_qr,
    qr_expiracion,
    comensales
)
VALUES
(
    2,
    'finalizada',
    TRUE,
    '20:00:00',
    '2026-05-20',
    TRUE,
    '00000000-0000-0000-0000-000000000001',
    'usado',
    '2026-05-20 22:00:00',
    2
),
(
    3,
    'finalizada',
    TRUE,
    '21:00:00',
    '2026-05-21',
    FALSE,
    '00000000-0000-0000-0000-000000000002',
    'usado',
    '2026-05-21 23:00:00',
    4
),
(
    4,
    'cancelada',
    FALSE,
    '13:00:00',
    '2026-05-22',
    TRUE,
    '00000000-0000-0000-0000-000000000003',
    'expirado',
    '2026-05-22 15:00:00',
    2
),
(
    5,
    'pendiente',
    FALSE,
    '20:30:00',
    '2026-05-28',
    TRUE,
    '00000000-0000-0000-0000-000000000004',
    'pendiente',
    '2026-05-28 22:30:00',
    6
),
(
    6,
    'pendiente',
    FALSE,
    '22:00:00',
    '2026-05-29',
    FALSE,
    '00000000-0000-0000-0000-000000000005',
    'pendiente',
    '2026-05-30 00:00:00',
    3
);

INSERT INTO reserva_mesa (
    id_reserva,
    id_mesa
)
VALUES
(1, 1),
(2, 7),
(3, 3),
(4, 5),
(5, 8);

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
    'Excelente atencion y muy buena comida.',
    'aprobada'
),
(
    3,
    2,
    4,
    'Muy rico todo aunque demoraron un poco.',
    'aprobada'
);