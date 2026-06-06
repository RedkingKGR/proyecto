from flask import Flask, render_template, request, redirect, session, jsonify
from database import crear_base_datos, agregar_usuario, verificar_usuario, obtener_usuario, actualizar_usuario
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar esto en producción

# Crear base de datos al iniciar
crear_base_datos()

@app.route('/')
def index():
    """Página de inicio"""
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        exitoso, resultado = verificar_usuario(email, contraseña)
        
        if exitoso:
            session['usuario_id'] = resultado['id']
            session['usuario_email'] = resultado['email']
            session['usuario_nombre'] = resultado['nombre']
            return redirect('/perfil')
        else:
            return render_template('login.html', error=resultado)
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        telefono = request.form.get('telefono')
        ciudad = request.form.get('ciudad')
        edad = request.form.get('edad')
        
        exitoso, mensaje = agregar_usuario(nombre, email, contraseña, telefono, ciudad, edad)
        
        if exitoso:
            return redirect('/login?mensaje=Registro exitoso. Inicia sesión')
        else:
            return render_template('registro.html', error=mensaje)
    
    return render_template('registro.html')

@app.route('/perfil')
def perfil():
    """Página de perfil del usuario (requiere login)"""
    if 'usuario_email' not in session:
        return redirect('/login')
    
    exitoso, usuario = obtener_usuario(session['usuario_email'])
    
    if exitoso:
        return render_template('perfil.html', usuario=usuario)
    else:
        return redirect('/login')

@app.route('/editar-perfil', methods=['GET', 'POST'])
def editar_perfil():
    """Editar información del perfil"""
    if 'usuario_email' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        ciudad = request.form.get('ciudad')
        edad = request.form.get('edad')
        
        exitoso, mensaje = actualizar_usuario(
            session['usuario_email'],
            nombre=nombre,
            telefono=telefono,
            ciudad=ciudad,
            edad=edad
        )
        
        if exitoso:
            return redirect('/perfil?mensaje=Perfil actualizado')
        else:
            return render_template('editar_perfil.html', error=mensaje)
    
    exitoso, usuario = obtener_usuario(session['usuario_email'])
    
    if exitoso:
        return render_template('editar_perfil.html', usuario=usuario)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect('/')

@app.route('/api/usuario')
def api_usuario():
    """API para obtener información del usuario (JSON)"""
    if 'usuario_email' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    exitoso, usuario = obtener_usuario(session['usuario_email'])
    
    if exitoso:
        return jsonify(usuario)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
