#!/bin/bash

# Script para ejecutar la aplicación Flask en Termux
# Autor: RedkingKGR
# Descripción: Inicia el servidor Flask de forma segura

echo "🚀 Iniciando aplicación Flask..."
echo "================================"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Ejecuta: pkg install python3"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip no está instalado"
    echo "Ejecuta: pkg install python3-pip"
    exit 1
fi

# Directorio del proyecto
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

echo "📂 Directorio del proyecto: $PROJECT_DIR"

# Crear directorio de base de datos si no existe
if [ ! -d "data" ]; then
    mkdir data
    echo "✓ Directorio 'data' creado"
fi

# Instalar dependencias si no están instaladas
echo ""
echo "📦 Verificando dependencias..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Crear la base de datos
echo ""
echo "🗄️ Creando base de datos..."
python3 database.py

if [ $? -eq 0 ]; then
    echo "✓ Base de datos creada/verificada"
else
    echo "❌ Error al crear la base de datos"
    exit 1
fi

# Iniciar el servidor Flask
echo ""
echo "================================"
echo "✓ Servidor iniciando..."
echo "📱 URL: http://localhost:5000"
echo "📱 URL: http://127.0.0.1:5000"
echo ""
echo "Para acceder desde otra máquina:"
echo "http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "================================"
echo ""

python3 app.py
