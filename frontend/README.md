# ReciclaYa Frontend

## Descripción

ConectaReciclaje Frontend es una aplicación web desarrollada con Angular que forma parte del sistema de reciclaje ReciclaYa. Esta aplicación permite a los ciudadanos reportar residuos para reciclaje, a los recicladores gestionar los reportes asignados, y a los supervisores administrar el sistema completo, incluyendo la gestión de usuarios, zonas y rutas de recolección.

## Tecnologías Utilizadas

- **Angular**: Framework principal para el desarrollo de la aplicación web.
- **Bootstrap**: Framework CSS para el diseño responsivo y componentes de interfaz.
- **TypeScript**: Lenguaje de programación utilizado para el desarrollo.
- **RxJS**: Para la gestión de operaciones asíncronas.
- **Angular CLI**: Herramienta para la construcción y gestión del proyecto.

## Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes programas:

- **Node.js**: Versión 18 o superior. Puedes descargarlo desde [nodejs.org](https://nodejs.org/).
- **npm**: Viene incluido con Node.js.
- **Angular CLI**: Instálalo globalmente con `npm install -g @angular/cli`.

## Instalación

Sigue estos pasos para instalar y configurar el proyecto:

1. Clona el repositorio o descarga los archivos del proyecto.
2. Navega al directorio del proyecto:
   ```bash
   cd frontend
   ```
3. Instala las dependencias:
   ```bash
   npm install
   ```

## Ejecutar el Proyecto en Desarrollo

Para ejecutar la aplicación en modo desarrollo:

```bash
ng serve
```

O usando el script definido en package.json:

```bash
npm start
```

La aplicación estará disponible en `http://localhost:4200/`. El servidor de desarrollo se recargará automáticamente cuando realices cambios en los archivos fuente.

Para ejecutar en un host específico (por ejemplo, para acceso desde otros dispositivos en la red):

```bash
ng serve --host 0.0.0.0 --port 4200
```

## Build de Producción

Para generar una versión optimizada para producción:

```bash
ng build
```

O usando el script definido:

```bash
npm run build
```

Los archivos compilados se almacenarán en el directorio `dist/recicla-ya-frontend/`. Esta versión está optimizada para rendimiento y puede ser desplegada en un servidor web.

## Estructura del Proyecto

```
recicla-ya-frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── menu-principal/          # Componente del menú principal
│   │   │   ├── perfil-usuario/          # Vista de perfil de usuario
│   │   │   ├── editar-usuario/          # Vista para editar perfil
│   │   │   ├── administracion/          # Vista de administración para supervisores
│   │   │   ├── gestion-reportes/        # Vista de gestión de reportes para recicladores
│   │   │   ├── reporte-ciudadano/       # Vista para reportes de ciudadanos
│   │   │   └── seguimiento/             # Vista de seguimiento de recolección
│   │   ├── app.config.ts                # Configuración de la aplicación
│   │   ├── app.routes.ts                # Definición de rutas
│   │   ├── app.html                     # Plantilla principal
│   │   └── app.ts                       # Componente raíz
│   ├── index.html                       # Archivo HTML principal
│   ├── main.ts                          # Punto de entrada
│   └── styles.scss                      # Estilos globales
├── public/                              # Archivos estáticos
├── angular.json                         # Configuración de Angular CLI
├── package.json                         # Dependencias y scripts
└── tsconfig.json                        # Configuración de TypeScript
```

## Vistas Implementadas

La aplicación cuenta con las siguientes vistas principales:

- **Menú Principal** (`/`): Página de inicio con navegación principal.
- **Perfil de Usuario** (`/perfil`): Vista para ver y gestionar el perfil del usuario actual.
- **Editar Usuario** (`/editar-perfil`): Formulario para editar la información del perfil.
- **Administración** (`/administracion`): Panel de administración para supervisores, incluye gestión de entidades del sistema.
- **Gestión de Reportes** (`/gestion-reportes`): Interfaz para recicladores para gestionar reportes asignados.
- **Reporte Ciudadano** (`/reporte-ciudadano`): Formulario para que ciudadanos reporten residuos para reciclaje.
- **Seguimiento** (`/seguimiento`): Vista para rastrear el estado de las recolecciones.

## Información de Contacto y Contribución

Para preguntas, reportes de bugs o contribuciones, puedes contactar al equipo de desarrollo.

- **Email**: [morenoquinterojaidersebastian@gmail.com]
- **Repositorio**: [https://github.com/Yulian4/ConectaReciclaje.git]

Si deseas contribuir al proyecto:
1. Haz un fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y commits.
4. Envía un pull request.

Asegúrate de seguir las guías de estilo del proyecto y ejecutar las pruebas antes de enviar tus contribuciones.
