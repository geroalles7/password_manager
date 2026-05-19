# 🔐 Password Manager

Password Manager es una aplicación de escritorio desarrollada en Python para la gestión segura de contraseñas personales.

Permite a múltiples usuarios almacenar, administrar y proteger sus credenciales mediante una contraseña maestra, utilizando cifrado fuerte para garantizar la privacidad de la información.

La aplicación funciona completamente offline, sin depender de servidores externos ni bases de datos remotas, manteniendo el control total de los datos en la computadora del usuario.

---

## ✨ Características

- Registro e inicio de sesión multiusuario
- Contraseña maestra por usuario
- Vault cifrado individual por usuario
- Agregar credenciales (sitio/app, usuario y contraseña)
- Editar credenciales existentes
- Eliminar credenciales
- Copiar usuario o contraseña al portapapeles
- Cambio de contraseña maestra
- Panel administrador para gestión de usuarios
- Interfaz gráfica moderna con tema oscuro
- Instalador para Windows
- Funcionamiento completamente offline

---

## 🔒 Seguridad

La aplicación implementa mecanismos modernos de seguridad:

- **Argon2** para hash seguro de contraseñas maestras
- **PBKDF2** para derivación de claves criptográficas
- **AES-GCM** para cifrado autenticado de los vaults
- Almacenamiento local cifrado por usuario

Cada usuario posee su propio archivo vault cifrado, por lo que las credenciales permanecen protegidas incluso si alguien accede directamente a los archivos almacenados.

---

## 🛠 Tecnologías utilizadas

- Python 3.11
- PySide6
- Cryptography
- Argon2-CFFI
- PyInstaller
- Inno Setup

---

## 🚀 Instalación

### Instalador para Windows

1. Descargar `PasswordManagerSetup.exe`
2. Ejecutar el instalador
3. Completar la instalación
4. Abrir la aplicación desde el acceso directo creado

---

## 💻 Ejecutar desde código fuente

Clonar repositorio:

```bash
git clone https://github.com/geroalles7/password_manager.git
cd password_manager
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual:

**Windows PowerShell**

```powershell
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python main.py
```

---

## 📁 Estructura del proyecto

```txt
password_manager/
│
├── assets/
│   ├── icon.ico
│   └── icon.png
│
├── core/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── config.py
│   ├── crypto_service.py
│   ├── models.py
│   └── storage_service.py
│
├── ui/
│   ├── __init__.py
│   ├── admin_dialog.py
│   ├── change_password_dialog.py
│   ├── dashboard.py
│   ├── login_window.py
│   ├── password_dialog.py
│   └── register_dialog.py
│
├── installer.iss
├── main.py
├── requirements.txt
├── version_info.txt
└── README.md
```

---

## 💾 Almacenamiento de datos

Los datos se almacenan localmente en Windows en:

```txt
%APPDATA%\PasswordManager
```

Ejemplo:

```txt
C:\Users\TuUsuario\AppData\Roaming\PasswordManager
```

Archivos generados:

- `users.json` → usuarios registrados
- `admin.vault` → vault del administrador
- `usuario.vault` → vault individual cifrado por usuario

---

## 👤 Usuario administrador

La aplicación incluye un usuario administrador por defecto.

Funciones disponibles:

- Ver usuarios registrados
- Eliminar usuarios
- Eliminar vaults asociados

---

## ⚠ Limitaciones actuales

- Disponible únicamente para Windows
- No incluye sincronización en la nube
- No incluye recuperación de contraseña maestra
- Si se elimina un archivo `.vault`, se pierden las credenciales asociadas

---

## 🔮 Futuras mejoras

- Exportar / importar credenciales
- Generador de contraseñas seguras
- Auto bloqueo por inactividad
- Limpieza automática del portapapeles
- Soporte para dispositivos móviles
- Backup cifrado

---

## 👨‍💻 Autor

**Alles Geronimo**

Proyecto desarrollado como solución de escritorio para gestión segura de contraseñas.

© 2026 Alles Geronimo. Todos los derechos reservados.
