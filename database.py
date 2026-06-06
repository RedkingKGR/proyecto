import sqlite3
import os

# Ruta de la base de datos
DB_PATH = 'usuarios.db'

def crear_base_datos():
    """Crea la base de datos y la tabla de usuarios si no existe"""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            telefono TEXT,
            ciudad TEXT,
            edad INTEGER,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conexion.commit()
    conexion.close()
    print("✓ Base de datos creada exitosamente")

def agregar_usuario(nombre, email, contraseña, telefono=None, ciudad=None, edad=None):
    """Agrega un nuevo usuario a la base de datos"""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, contraseña, telefono, ciudad, edad)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, email, contraseña, telefono, ciudad, edad))
        
        conexion.commit()
        conexion.close()
        return True, "Usuario registrado exitosamente"
    except sqlite3.IntegrityError:
        return False, "El email ya está registrado"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verificar_usuario(email, contraseña):
    """Verifica si el usuario y contraseña son correctos"""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute('''
            SELECT id, nombre, email FROM usuarios 
            WHERE email = ? AND contraseña = ?
        ''', (email, contraseña))
        
        usuario = cursor.fetchone()
        conexion.close()
        
        if usuario:
            return True, {"id": usuario[0], "nombre": usuario[1], "email": usuario[2]}
        else:
            return False, "Email o contraseña incorrectos"
    except Exception as e:
        return False, f"Error: {str(e)}"

def obtener_usuario(email):
    """Obtiene la información de un usuario por email"""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        conexion.close()
        
        if usuario:
            return True, {
                "id": usuario[0],
                "nombre": usuario[1],
                "email": usuario[2],
                "telefono": usuario[4],
                "ciudad": usuario[5],
                "edad": usuario[6],
                "fecha_registro": usuario[7]
            }
        else:
            return False, "Usuario no encontrado"
    except Exception as e:
        return False, f"Error: {str(e)}"

def actualizar_usuario(email, nombre=None, telefono=None, ciudad=None, edad=None):
    """Actualiza la información de un usuario"""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        updates = []
        valores = []
        
        if nombre:
            updates.append("nombre = ?")
            valores.append(nombre)
        if telefono:
            updates.append("telefono = ?")
            valores.append(telefono)
        if ciudad:
            updates.append("ciudad = ?")
            valores.append(ciudad)
        if edad:
            updates.append("edad = ?")
            valores.append(edad)
        
        if not updates:
            return False, "No hay datos para actualizar"
        
        valores.append(email)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE email = ?"
        
        cursor.execute(query, valores)
        conexion.commit()
        conexion.close()
        
        return True, "Usuario actualizado exitosamente"
    except Exception as e:
        return False, f"Error: {str(e)}"

if __name__ == "__main__":
    crear_base_datos()
