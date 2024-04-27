-- Creación de la tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    usuario VARCHAR PRIMARY KEY,  
    -- Identificador único del usuario
    nombre VARCHAR NOT NULL,      
    -- Nombre del usuario
    email VARCHAR,                
    -- Dirección de correo electrónico del usuario
    clave VARCHAR NOT NULL   
    -- Contraseña del usuario
);

-- Creación de la tabla vehiculos
CREATE TABLE IF NOT EXISTS vehiculos (
    placa VARCHAR PRIMARY KEY,        
    -- Número de placa del vehículo (clave primaria)
    tipo VARCHAR NOT NULL,            
    -- Tipo de vehículo (por ejemplo, automóvil, camión, etc.)
    marca VARCHAR NOT NULL,           
    -- Marca del vehículo
    modelo INT NOT NULL,              
    -- Año del modelo del vehículo
    capacidad DECIMAL(6,2) NOT NULL,  
    -- Capacidad de carga o pasajeros del vehículo
    kilometraje INT NOT NULL,         
    -- Kilometraje actual del vehículo
    combustible VARCHAR NOT NULL,     
    -- Tipo de combustible utilizado por el vehículo
    rendimiento DECIMAL(6,2),         
    -- Rendimiento en kilómetros por litro del vehículo
    descripcion VARCHAR,              
    -- Descripción adicional del vehículo
    propietario VARCHAR NOT NULL,     
    -- Usuario propietario del vehículo (clave foránea)
    FOREIGN KEY (propietario) REFERENCES usuarios(usuario)  
    -- Restricción de integridad referencial
);

-- Creación de la tabla conductores
CREATE TABLE IF NOT EXISTS conductores (
    id SERIAL PRIMARY KEY,           
    -- Identificador único del conductor (clave primaria)
    nombre VARCHAR NOT NULL,         
    -- Nombre del conductor
    vehiculo VARCHAR NOT NULL,       
    -- Número de placa del vehículo asignado al conductor (clave foránea)
    descripcion VARCHAR,             
    -- Descripción adicional del conductor
    propietario VARCHAR NOT NULL,    
    -- Usuario propietario del conductor (clave foránea)
    FOREIGN KEY (vehiculo) REFERENCES vehiculos(placa),  
    -- Restricción de integridad referencial
    FOREIGN KEY (propietario) REFERENCES usuarios(usuario)  
    -- Restricción de integridad referencial
);

-- Creación de la tabla pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,           
    -- Identificador único del pedido (clave primaria)
    direccion VARCHAR NOT NULL,      
    -- Dirección de entrega del pedido
    fecha TIMESTAMP NOT NULL,        
    -- Fecha y hora de realización del pedido
    cliente VARCHAR NOT NULL,        
    -- Usuario cliente que realizó el pedido (clave foránea)
    estado VARCHAR NOT NULL,         
    -- Estado actual del pedido (por ejemplo, pendiente, entregado, etc.)
    descripcion VARCHAR,             
    -- Descripción adicional del pedido
    propietario VARCHAR NOT NULL,    
    -- Usuario propietario del pedido (clave foránea)
    FOREIGN KEY (propietario) REFERENCES usuarios(usuario)  
    -- Restricción de integridad referencial
);

-- Creación de la tabla acc_cond_combustible
CREATE TABLE IF NOT EXISTS acc_cond_combustible (
    id SERIAL PRIMARY KEY,           
    -- Identificador único de la acción de combustible (clave primaria)
    conductor INT NOT NULL,          
    -- Identificador único del conductor que realizó la acción (clave foránea)
    vehiculo VARCHAR NOT NULL,      
    -- Placa del vehículo en el que se realizó la acción (clave foránea)
    galones DECIMAL(6,2) NOT NULL,  
    -- Cantidad de galones de combustible añadidos
    kilometraje INT NOT NULL,       
    -- Kilometraje del vehículo al momento de la acción
    fecha TIMESTAMP NOT NULL,       
    -- Fecha y hora de la acción
    hora TIME,                      
    -- Hora de la acción
    descripcion VARCHAR,            
    -- Descripción adicional de la acción
    propietario VARCHAR NOT NULL,   
    -- Usuario propietario de la acción (clave foránea)
    FOREIGN KEY (conductor) REFERENCES conductores(id),    
    -- Restricción de integridad referencial
    FOREIGN KEY (vehiculo) REFERENCES vehiculos(placa),    
    -- Restricción de integridad referencial
    FOREIGN KEY (propietario) REFERENCES usuarios(usuario)  
    -- Restricción de integridad referencial
);

-- Creación de la tabla acc_cond_pedidos
CREATE TABLE IF NOT EXISTS acc_cond_pedidos (
    id SERIAL PRIMARY KEY,           
    -- Identificador único de la acción de pedido (clave primaria)
    conductor INT NOT NULL,          
    -- Identificador único del conductor que realizó la acción (clave foránea)
    vehiculo VARCHAR NOT NULL,      
    -- Número de placa del vehículo asociado a la acción (clave foránea)
    fecha TIMESTAMP NOT NULL,       
    -- Fecha y hora de la acción
    hora TIME,                      
    -- Hora de la acción
    pedido INT NOT NULL,            
    -- Identificador único del pedido asociado a la acción (clave foránea)
    descripcion VARCHAR,            
    -- Descripción adicional de la acción
    propietario VARCHAR NOT NULL,   
    -- Usuario propietario de la acción (clave foránea)
    FOREIGN KEY (conductor) REFERENCES conductores(id),    
    -- Restricción de integridad referencial
    FOREIGN KEY (vehiculo) REFERENCES vehiculos(placa),    
    -- Restricción de integridad referencial
    FOREIGN KEY (pedido) REFERENCES pedidos(id),           
    -- Restricción de integridad referencial
    FOREIGN KEY (propietario) REFERENCES usuarios(usuario)  
    -- Restricción de integridad referencial
);
