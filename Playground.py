import sqlite3
import os

DB_NAME = ":memory:"

# 1. Esquema DDL
SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS BEBEDOR (
  CI VARCHAR(20) PRIMARY KEY,
  Nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS FUENTE_SODA (
    CodFS VARCHAR(10) PRIMARY KEY,
    NombreFS VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS BEBIDA (
    CodBeb VARCHAR(10) PRIMARY KEY,
    NombreBeb VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS FRECUENTA (
    CI VARCHAR(20) REFERENCES BEBEDOR(CI) ON DELETE CASCADE,
    CodFS VARCHAR(10) REFERENCES FUENTE_SODA(CodFS) ON DELETE CASCADE,
    PRIMARY KEY (CI, CodFS)
);

CREATE TABLE IF NOT EXISTS GUSTA (
    CI VARCHAR(20) REFERENCES BEBEDOR(CI) ON DELETE CASCADE,
    CodBeb VARCHAR(10) REFERENCES BEBIDA(CodBeb) ON DELETE CASCADE,
    PRIMARY KEY (CI, CodBeb)
);

CREATE TABLE IF NOT EXISTS VENDE (
    CodFS VARCHAR(10) REFERENCES FUENTE_SODA(CodFS) ON DELETE CASCADE,
    CodBeb VARCHAR(10) REFERENCES BEBIDA(CodBeb) ON DELETE CASCADE,
    Precio DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (CodFS, CodBeb)
);
CREATE TABLE IF NOT EXIST EASTER_EGG (
    CodEgg VARCHAR(10) PRIMARY KEY,
    Easter VARCHAR(100) NOT NULL
)
"""
# Fin del Esquema DDL

# Datos iniciales
SEED_SQL = """
INSERT OR IGNORE INTO BEBEDOR VALUES 
    ('V-1', 'Luis Pérez'),
    ('V-2', 'José Pérez'),
    ('V-3', 'Maria Gomez'),
    ('V-4', 'Carlos Rodriguez'),
    ('V-7', 'Jose Torbet');

INSERT OR IGNORE INTO FUENTE_SODA VALUES 
    ('FS1', 'El Punto'),
    ('FS2', 'El Ávila'),
    ('FS3', 'Tu Conuco');

INSERT OR IGNORE INTO BEBIDA VALUES 
    ('B1', 'Malta'),
    ('B2', 'Frescolita'),
    ('B3', 'Coca-Cola'),
    ('B4', 'Jugo de Naranja');

INSERT OR IGNORE INTO FRECUENTA VALUES 
    ('V-1', 'FS1'), ('V-1', 'FS2'),
    ('V-2', 'FS1'),
    ('V-3', 'FS2'), ('V-3', 'FS3');

INSERT OR IGNORE INTO GUSTA VALUES 
    ('V-1', 'B1'), ('V-1', 'B2'),
    ('V-2', 'B1'), ('V-2', 'B3'),
    ('V-3', 'B1'), ('V-3', 'B4');

INSERT OR IGNORE INTO VENDE VALUES 
    ('FS1', 'B1', 2.50), ('FS1', 'B2', 2.00), ('FS1', 'B3', 2.20),
    ('FS2', 'B1', 2.80), ('FS2', 'B4', 3.00),
    ('FS3', 'B2', 1.80), ('FS3', 'B3', 2.00);

INSERT OR IGNORE INTO EASTER_EGG VALUES
    ('Egg1', 'Yo solía ser un aventurero como tú. Pero un día me hirieron en la rodilla con una flecha.'),
    ('Egg2', 'There are no easter eggs up here. Go away.'),
    ('Egg3', 'The cake is a lie.');
"""
# Fin de Datos Iniciales

# Inicio SQL
def init_db(conn):
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    cursor.executescript(SEED_SQL)
    conn.commit()
    print("Base de datos inicializada con esquema y datos de prueba.")

def imprimir_tabla(columnas, filas):
    if not filas:
        print("(0 filas devueltas)")
        return
    
    # Calcular ancho de columnas para formato alineado
    widths = [len(str(col)) for col in columnas]
    for fila in filas:
        for i, val in enumerate(fila):
            widths[i] = max(widths[i], len(str(val if val is not None else "NULL")))
    
    row_format = " | ".join(["{:<" + str(w) + "}" for w in widths])
    linea_sep = "-+-".join(["-" * w for w in widths])
    
    print(row_format.format(*columnas))
    print(linea_sep)
    for fila in filas:
        valores_str = [str(v) if v is not None else "NULL" for v in fila]
        print(row_format.format(*valores_str))
    print(f"\n({len(filas)} fila(s) devuelta(s))")

def main():
    conn = sqlite3.connect(DB_NAME)
    # Activar restricciones de llaves foráneas en SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    
    init_db(conn)
    
    print("\n=======================================================")
    print("  ZoneJack Presenta - Practica de Base de Datos   ")
    print("Datos y Esquema Relacional de la guía de Ejercicios de Álgebra y Cálculo Relacional")
    print("Del Departamento de Computación y T.I. - Universidad Simón Bolívar")
    print("=======================================================")
    print("• Escribe tus consultas SQL (SELECT, INSERT, UPDATE, DELETE).")
    print("• Escribe 'SALIR' o 'EXIT' para terminar.")
    print("• Escribe 'TABLAS' para ver la lista de tablas.")
    print("=======================================================\n")

    while True:
        try:
            # Captura de consulta multilínea opcional o simple
            query = input("SQL> ").strip()
            
            if not query:
                continue
            
            if query.upper() in ["SALIR", "EXIT", "QUIT"]:
                print("¡Hasta luego!")
                break

            if query.upper() == "TABLAS":
                query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"

            cursor = conn.cursor()
            cursor.execute(query)

            # Si es SELECT o devuelve filas
            if cursor.description:
                columnas = [desc[0] for desc in cursor.description]
                resultados = cursor.fetchall()
                print("\n[ÉXITO] Consulta ejecutada correctamente:\n")
                imprimir_tabla(columnas, resultados)
                print()
            else:
                # Si es INSERT, UPDATE, DELETE, CREATE, etc.
                conn.commit()
                print(f"\n[ÉXITO] Operación ejecutada correctamente. Filas afectadas: {cursor.rowcount}\n")

        except sqlite3.Error as e:
            print(f"\n[ERROR SQL]: {e}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta luego!")
            break

    conn.close()

if __name__ == "__main__":
    main()
