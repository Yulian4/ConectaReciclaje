![Logo de ConectaReciclaje](banner.png)

<!-- Reemplaza la ruta por tu imagen (por ejemplo: docs/images/logo.png) -->
# ConectaReciclaje

## Descripción General

ConectaReciclaje es una plataforma integral para la gestión de reportes de materiales reciclables. Permite a los ciudadanos reportar materiales disponibles para reciclaje y conecta automáticamente con recicladores locales mediante notificaciones SMS. El sistema utiliza una arquitectura de microservicios con agentes inteligentes basados en MCP (Model Context Protocol) y un backend REST API en Spring Boot.

## Arquitectura del Sistema

### Componentes Principales

1. **Backend (Spring Boot)**
   - API REST para autenticación y gestión de reportes
   - Base de datos MySQL con JPA/Hibernate
   - Autenticación JWT
   - Filtros de seguridad y CORS

2. **Agentes MCP (Python)**
   - **Agente Ciudadano**: Maneja reportes de ciudadanos, inserción en BD y notificaciones SMS
   - **Agente Reciclador**: Consulta reportes disponibles y acepta asignaciones
   - **Agente Orquestador**: Coordina las comunicaciones entre agentes

3. **Frontend (HTML/CSS/JavaScript)**
   - Interfaz de usuario para login, registro y chat
   - Comunicación con backend vía REST API

## Estructura del Proyecto

```
ConectaReciclaje/
├── Agentes/                          # Agentes MCP en Python
│   ├── ciudadano/                    # Agente para ciudadanos
│   │   ├── server.py                 # Servidor MCP con herramientas
│   │   ├── client.py                 # Cliente con LLM (Gemini)
│   │   ├── notificador.py            # (Vacío)
│   │   ├── pyproject.toml            # Dependencias Python
│   │   ├── .env.example              # Variables de entorno
│   │   └── README.md                 # (Vacío)
│   ├── notificador/                  # Agente notificador (básico)
│   ├── orquestador/                  # Agente coordinador
│   │   ├── server.py                 # Servidor MCP de transferencia
│   │   ├── client.py                 # Cliente FastAPI para orquestación
│   │   └── .env.example
│   └── reciclador/                  # Agente para recicladores
│       ├── server.py                 # Servidor MCP con consultas
│       └── client.py                 # Cliente con WebSocket
├── backend/                          # Backend Spring Boot
│   └── ConnectaReciclaje/
│       ├── pom.xml                   # Dependencias Maven
│       ├── src/main/java/com/api/connect/
│       │   ├── ConnectaReciclajeApplication.java
│       │   ├── config/               # Configuraciones
│       │   │   ├── AppConfig.java
│       │   │   ├── CorsConfig.java
│       │   │   └── FilterConfig.java
│       │   ├── controller/           # Controladores REST
│       │   │   ├── AuthController.java
│       │   │   └── ReporteController.java
│       │   ├── dto/                  # Objetos de transferencia
│       │   ├── entity/               # Entidades JPA
│       │   │   ├── User.java
│       │   │   ├── Adress.java
│       │   │   └── Town.java
│       │   ├── filter/               # Filtros de servlet
│       │   │   └── JwtValidationFilter.java
│       │   ├── repository/           # Repositorios JPA
│       │   ├── service/              # Servicios de negocio
│       │   │   ├── AuthService.java
│       │   │   ├── JwtService.java
│       │   └── └── ReporteService.java
│       └── src/main/resources/
│           ├── application.properties
│           └── application.yml
├── frontend/                         # Frontend web
│   ├── index.html                    # Login
│   ├── register.html                 # Registro
│   ├── principal.html                # Página principal
│   ├── chat.html                     # Chat con bot
│   ├── css/                          # Estilos CSS
│   └── js/                           # JavaScript
├── docs/                             # Documentación
└── qa/                               # Pruebas de calidad
```

## Tecnologías Utilizadas

### Backend
- **Java 17**
- **Spring Boot 3.5.6**
- **Spring Security Crypto**
- **JWT (JJWT)**
- **MySQL Connector**
- **JPA/Hibernate**
- **Lombok**

### Agentes MCP
- **Python 3.12+**
- **FastMCP** (para servidores MCP)
- **Mirascope** (integración con LLMs)
- **Google Gemini 2.5 Pro**
- **WebSockets** (para comunicación en tiempo real)
- **Twilio** (para SMS)
- **MySQL Connector**

### Frontend
- **HTML5**
- **CSS3** (con gradientes y diseño moderno)
- **JavaScript** (ES6+)
- **Fetch API** (para llamadas HTTP)

### Base de Datos
- **MySQL 8.0**
- **Hibernate DDL Auto: update**

## Funcionalidades Principales

### Para Ciudadanos
1. **Registro y Login**: Autenticación segura con JWT
2. **Crear Reportes**: Reportar materiales reciclables disponibles
3. **Notificaciones Automáticas**: SMS a recicladores locales
4. **Consultar Reportes**: Ver historial de reportes propios

### Para Recicladores
1. **Registro y Login**: Autenticación por rol
2. **Consultar Reportes Cercanos**: Ver materiales disponibles en su barrio
3. **Aceptar Asignaciones**: Programar recogidas de materiales
4. **Comunicación en Tiempo Real**: WebSocket para interacciones

### Sistema de Notificaciones
- **SMS Automáticos**: Envío de notificaciones vía Twilio
- **Localización**: Basado en barrios/direcciones
- **Coordinación**: Orquestador maneja el flujo entre agentes

## Configuración y Instalación

### Prerrequisitos
- Java 17+
- Python 3.12+
- MySQL 8.0+
- Node.js (opcional, para desarrollo frontend)
- Cuenta Twilio (para SMS)

### Configuración de Base de Datos

```sql
-- Crear base de datos
CREATE DATABASE conectarecicla;

-- Tablas principales (creadas automáticamente por Hibernate)
-- usuarios, direccion, barrio, reportes, materiales, asignaciones
```

### Variables de Entorno

#### Backend (.env o application.yml)
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/conectarecicla
    username: root
    password: tu_password
  jpa:
    hibernate:
      ddl-auto: update
security:
  jwt:
    secret-key: "tu_clave_secreta_jwt"
    expiration: 3600000
```

#### Agentes Python (.env)
```env
GOOGLE_API_KEY=tu_api_key_gemini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=conectarecicla
TWILIO_SID=tu_sid_twilio
TWILIO_TOKEN=tu_token_twilio
TWILIO_PHONE=+1234567890
```

### Instalación y Ejecución

#### Backend
```bash
cd backend/ConnectaReciclaje
mvn clean install
mvn spring-boot:run
```

#### Agentes
```bash
# Agente Ciudadano
cd Agentes/ciudadano
uv run server.py

# Agente Reciclador
cd Agentes/reciclador
uv run server.py

# Agente Orquestador
cd Agentes/orquestador
uv run client.py
```

#### Frontend
```bash
# Servir archivos estáticos (usando Python simple server)
cd frontend
python -m http.server 5500
```

## API Endpoints

### Autenticación
- `POST /auth/register` - Registro de usuarios
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token

### Reportes
- `POST /api/reportes` - Crear reporte (requiere JWT)

## Flujo de Trabajo

1. **Usuario se registra** como ciudadano o reciclador
2. **Ciudadano crea reporte** vía chat o API
3. **Sistema identifica material** y ubicación
4. **Agente Ciudadano** inserta en BD y envía SMS
5. **Recicladores reciben notificación** automática
6. **Reciclador consulta reportes** disponibles
7. **Reciclador acepta asignación** con fecha/hora
8. **Sistema confirma** la asignación

## Arquitectura MCP

Los agentes utilizan el **Model Context Protocol (MCP)** para comunicación estructurada:

- **Servidores MCP**: Proporcionan herramientas específicas
- **Clientes MCP**: Ejecutan herramientas vía WebSocket/HTTP
- **LLM Integration**: Gemini 2.5 Pro analiza consultas naturales
- **Orquestador**: Coordina llamadas entre agentes

## Seguridad

- **JWT Tokens**: Autenticación stateless
- **Filtros de Seguridad**: Validación de tokens en endpoints protegidos
- **CORS**: Configurado para desarrollo local
- **Password Encoding**: BCrypt para contraseñas
- **Validación de Roles**: Diferentes permisos por tipo de usuario

## Desarrollo y Testing

### Testing
- **JUnit** para backend Java
- **Spring Boot Test** para integración
- Archivos en `qa/` para pruebas de calidad

### Debugging
- Logs detallados en backend
- Modo debug en agentes Python
- Consola del navegador para frontend

## Despliegue (en proceso)

### Producción
- Configurar variables de entorno reales
- Usar HTTPS en producción
- Configurar CORS para dominio específico
- Base de datos dedicada
- Servicios en contenedores Docker

### Docker (en proceso)
```dockerfile
# Dockerfile para backend
FROM openjdk:17-jdk-alpine
COPY target/*.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

## Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

- **Jaider Moreno**: morenoquinterojaidersebastian@gmail.com 
- **Yuliana Yate**: yulsyay19@gmail.com 
- **Dunkan Hernandez**: dnicolas.hr.98@gmail.com

---

**Estado del Proyecto**: En desarrollo activo
**Versión**: 0.1.0
**Última Actualización**: 2025




