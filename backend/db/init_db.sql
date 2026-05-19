CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,

    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,

    es_admin BOOLEAN DEFAULT FALSE,

    reservas INT DEFAULT 0,
    canceladas INT DEFAULT 0
);

CREATE TABLE categoria_plato (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,

    categoria VARCHAR(50) NOT NULL
);

CREATE TABLE plato (
    id_plato INT PRIMARY KEY AUTO_INCREMENT,

    id_categoria INT,

    nombre VARCHAR(50) NOT NULL,
    link_imagen VARCHAR(500) NOT NULL,

    precio DECIMAL(10,2) NOT NULL,

    hay_stock BOOLEAN DEFAULT TRUE,

    gluten BOOLEAN DEFAULT FALSE,
    producto_animal BOOLEAN DEFAULT FALSE,
    carnes BOOLEAN DEFAULT FALSE,
    lactosa BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_plato_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categoria_plato(id_categoria)
        ON DELETE SET NULL
);

CREATE TABLE reserva (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,

    id_usuario INT,

    interior BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    fecha DATETIME NOT NULL,

    codigo_qr VARCHAR(500) NOT NULL,

    comensales INT NOT NULL,

    CONSTRAINT fk_reserva_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE SET NULL
);

CREATE TABLE configuracion (
    clave VARCHAR(100) PRIMARY KEY,

    valor TEXT
);

CREATE TABLE servicios_extra (
    id_servicio INT PRIMARY KEY AUTO_INCREMENT,

    nombre VARCHAR(100) NOT NULL,

    descripcion VARCHAR(500),

    disponible BOOLEAN DEFAULT TRUE
);

CREATE TABLE mesa (
    id_mesa INT PRIMARY KEY AUTO_INCREMENT,

    numero INT UNIQUE,

    capacidad INT NOT NULL,

    interior BOOLEAN DEFAULT TRUE,
    funcional BOOLEAN DEFAULT TRUE
);

CREATE TABLE reserva_mesa (
    id_reserva INT,
    id_mesa INT,

    estado ENUM(
        'pendiente',
        'cancelada',
        'finalizada'
    ) DEFAULT 'pendiente',

    reseñada BOOLEAN DEFAULT FALSE,

    hora_reserva TIMESTAMP,

    fecha DATETIME DEFAULT (CURRENT_DATE),

    PRIMARY KEY (id_reserva, id_mesa),

    CONSTRAINT fk_reserva_mesa_reserva
        FOREIGN KEY (id_reserva)
        REFERENCES reserva(id_reserva)
        ON DELETE CASCADE,

    CONSTRAINT fk_reserva_mesa_mesa
        FOREIGN KEY (id_mesa)
        REFERENCES mesa(id_mesa)
        ON DELETE CASCADE
);

CREATE TABLE reseña (
    id_reseña INT PRIMARY KEY AUTO_INCREMENT,

    id_usuario INT,
    id_reserva INT,

    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    calificacion INT NOT NULL
        CHECK (calificacion BETWEEN 1 AND 5),

    comentario TEXT,

    estado ENUM(
        'no_revisada',
        'no_aprobada',
        'aprobada'
    ) DEFAULT 'no_revisada',

    CONSTRAINT fk_reseña_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE SET NULL,

    CONSTRAINT fk_reseña_reserva
        FOREIGN KEY (id_reserva)
        REFERENCES reserva(id_reserva)
        ON DELETE CASCADE
);

-- DATOS INICIALES

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
    es_admin
)
VALUES (
    'admin@puertohermoso.com',
    '1234',
    TRUE
);


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