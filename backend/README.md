♻️ Backend - ConectaReciclaje
🧭 Descripción General

El backend de ConectaReciclaje es el núcleo lógico de la aplicación.
Su función principal es autenticar usuarios, procesar peticiones HTTP, manejar datos con la base de datos MySQL y ofrecer servicios REST para la interacción entre ciudadanos y el sistema de reciclaje.

A diferencia del frontend, que muestra la interfaz al usuario, este backend se encarga de:

Validar credenciales de usuario.

Proteger rutas mediante JWT.

Procesar solicitudes (registro, login, reportes, etc).

Interactuar con la base de datos usando JPA.

⚙️ Stack Tecnológico
Tecnología	Función Principal
Java 17	Lenguaje de programación base del proyecto.
Spring Boot 3.5.6	Framework que simplifica la creación de aplicaciones Java empresariales.
Spring Web (spring-boot-starter-web)	Permite crear controladores REST que reciben y responden peticiones HTTP.
Spring Data JPA	Conecta el proyecto con la base de datos usando entidades Java (ORM).
Spring Security + Crypto	Proporciona autenticación, autorización y encriptación de contraseñas.
JWT (io.jsonwebtoken)	Maneja sesiones seguras con tokens para identificar usuarios autenticados.
MySQL	Base de datos relacional donde se almacenan usuarios y reportes.
Maven	Gestiona dependencias y permite compilar y ejecutar el proyecto fácilmente.
Lombok	Reduce el código repetitivo con anotaciones automáticas para getters, setters y constructores.
🧩 Dependencias y su Propósito
🔒 Seguridad y Autenticación
<dependency>
  <groupId>org.springframework.security</groupId>
  <artifactId>spring-security-crypto</artifactId>
</dependency>


➡️ Permite encriptar contraseñas con algoritmos seguros como BCrypt antes de guardarlas en la base de datos.
Se usa dentro del servicio de autenticación (AuthService).

🧭 Controladores REST y Lógica Web
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>


➡️ Habilita Spring MVC, el motor que permite crear endpoints como /auth/login o /api/reportes.
Define controladores con anotaciones como @RestController y @PostMapping.

🧠 Persistencia y Conexión a la Base de Datos
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>


➡️ Integra Java Persistence API (JPA) y Hibernate para trabajar con entidades Java en lugar de escribir SQL manual.
Ejemplo: al guardar un usuario, JPA convierte el objeto Java en una fila en la tabla correspondiente.

🐬 Conector MySQL
<dependency>
  <groupId>com.mysql</groupId>
  <artifactId>mysql-connector-j</artifactId>
  <scope>runtime</scope>
</dependency>


➡️ Es el driver JDBC que permite que la aplicación se comunique directamente con la base de datos MySQL.
Sin él, la conexión jdbc:mysql://... no funcionaría.

🔑 Manejo de Tokens JWT
<dependency>
  <groupId>io.jsonwebtoken</groupId>
  <artifactId>jjwt-api</artifactId>
  <version>0.11.5</version>
</dependency>
<dependency>
  <groupId>io.jsonwebtoken</groupId>
  <artifactId>jjwt-impl</artifactId>
  <version>0.11.5</version>
  <scope>runtime</scope>
</dependency>
<dependency>
  <groupId>io.jsonwebtoken</groupId>
  <artifactId>jjwt-jackson</artifactId>
  <version>0.11.5</version>
  <scope>runtime</scope>
</dependency>


➡️ Permite generar, firmar y validar tokens JWT, que se usan para autenticar usuarios sin guardar sesiones en el servidor.
Cuando un usuario inicia sesión correctamente, se genera un token que debe enviarse en cada petición posterior.

✂️ Reducción de Código Boilerplate
<dependency>
  <groupId>org.projectlombok</groupId>
  <artifactId>lombok</artifactId>
  <optional>true</optional>
</dependency>


➡️ Elimina la necesidad de escribir manualmente getters, setters, constructores, etc., mediante anotaciones como:

@Data
@RequiredArgsConstructor
public class Usuario { ... }

🧰 Requisitos Previos

Java 17 o superior

Maven 3.6+

MySQL 8.0+ (con base de datos conectarecicla)

Lombok instalado en tu IDE (VSCode, IntelliJ o Eclipse)

💻 IDEs Recomendados

Puedes abrir el proyecto con:

🧩 Visual Studio Code (con extensiones Java y Lombok activadas)

☕ Eclipse IDE for Enterprise Java

🚀 IntelliJ IDEA Community / Ultimate

⚙️ Configuración del Proyecto
1️⃣ Clonar el repositorio
git clone <url-del-repositorio>
cd ConectaReciclaje/backend

2️⃣ Crear la base de datos en MySQL
CREATE DATABASE conectarecicla;

3️⃣ Configurar credenciales en application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/conectarecicla?useSSL=false&serverTimezone=UTC
    username: tu_usuario
    password: tu_contraseña
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true

jwt:
  secret: EstaEsUnaLlaveSuperSecretaParaJWT123456789
  expiration: 3600000 # 1 hora

🚀 Ejecución del Proyecto
En modo desarrollo
mvn spring-boot:run

En modo producción
mvn clean package
java -jar target/conectareciclaje-0.0.1-SNAPSHOT.jar


Accede en tu navegador o Postman a:
👉 http://localhost:8080

🧪 Pruebas con Postman
🔐 Autenticación
➕ Registro de usuario

POST /auth/register

{
  "nombreCompleto": "Yuliana Yate",
  "tipoDoc": "CC",
  "numeroDoc": "1234567890",
  "telefono": "+573227470254",
  "email": "yuli2@example.com",
  "password": "12345",
  "rol": "CIUDADANO",
  "idDireccion": 1
}

🔑 Inicio de sesión

POST /auth/login

{
  "email": "yuli2@example.com",
  "password": "12345"
}


📥 Devuelve un token JWT:

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5..."
}

🔁 Refrescar token

POST /auth/refresh
Encabezado:
Authorization: Bearer <token>

♻️ Reportes Ciudadanos
📤 Crear reporte

POST /api/reportes
Encabezado:
Authorization: Bearer <token>
Body:

{
  "query": "quiero hacer un reporte"
}


✅ Si el token es válido, responde:

{
  "mensaje": "Reporte enviado con éxito"
}

🧱 Estructura del Proyecto
src/main/java/com/api/conecta/
├── config/           # Configuración de seguridad y JWT
├── controller/       # Controladores REST (AuthController, ReporteController)
├── dto/              # Objetos de transferencia de datos (Request y Response)
├── entity/           # Entidades JPA que representan tablas
├── filter/           # Filtros de validación de tokens JWT
├── repository/       # Repositorios JPA para acceso a datos
└── service/          # Lógica de negocio y reglas de validación

🔒 Seguridad

Spring Security gestiona autenticación y autorización.

Contraseñas encriptadas con BCrypt.

JWT protege rutas privadas.

Los tokens se validan automáticamente mediante un filtro antes de permitir el acceso a /api/**.

🧾 Logging

Hibernate muestra las consultas SQL en la consola.

Niveles DEBUG y TRACE habilitados para depuración.

🤝 Contribución

Crea una rama: git checkout -b feature/nueva-funcionalidad

Realiza tus cambios y pruébalos.

Haz un commit: git commit -m "Agregada nueva funcionalidad"

Envía tu Pull Request.

📜 Licencia

Proyecto de código abierto bajo la licencia MIT.
Puedes usarlo, modificarlo y distribuirlo libremente.
