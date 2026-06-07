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

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    
    estado_reserva ENUM(
        'pendiente',
        'cancelada',
        'finalizada'
    ) DEFAULT 'pendiente' NOT NULL, 

    reseñada BOOLEAN DEFAULT FALSE NOT NULL,

    hora_reserva TIME NOT NULL,

    fecha DATE DEFAULT (CURRENT_DATE) NOT NULL,

    interior BOOLEAN DEFAULT TRUE NOT NULL,

    uuid_qr CHAR(36) not null UNIQUE,

    estado_qr ENUM(
        'pendiente',
        'usado',
        'expirado'
    ) DEFAULT 'pendiente',
 
    qr_expiracion TIMESTAMP NOT NULL,
    
    comensales INT NOT NULL,

    
    estado_reserva ENUM(
        'pendiente',
        'cancelada',
        'finalizada'
    ) DEFAULT 'pendiente' NOT NULL, 

    reseñada BOOLEAN DEFAULT FALSE NOT NULL,

    hora_reserva TIME NOT NULL,

    fecha DATE DEFAULT (CURRENT_DATE) NOT NULL,

    interior BOOLEAN DEFAULT TRUE NOT NULL,

    uuid_qr CHAR(36) not null UNIQUE,

    estado_qr ENUM(
        'pendiente',
        'usado',
        'expirado'
    ) DEFAULT 'pendiente',
 
    qr_expiracion TIMESTAMP NOT NULL,
    
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

    numero INT UNIQUE NOT NULL,

    capacidad INT NOT NULL,

    interior BOOLEAN DEFAULT TRUE NOT NULL,
    funcional BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE reserva_mesa (
    id_reserva INT,
    id_mesa INT,
    PRIMARY KEY (id_reserva, id_mesa),

    CONSTRAINT fk_reserva_mesa_reserva
        FOREIGN KEY (id_reserva)
        REFERENCES reserva(id_reserva)
        ON DELETE CASCADE,

    CONSTRAINT fk_reserva_mesa_mesa
        FOREIGN KEY (id_mesa)
        REFERENCES mesa(id_mesa)
        ON DELETE SET NULL
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
