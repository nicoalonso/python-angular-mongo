# Library Backend

Este es el backend de la aplicación de biblioteca.

## Tecnologías

- Python con el Framework FastAPI
- MongoDB como BD
- RabbitMQ como capa de transporte
- Arquitectura Hexagonal

## Swagger

La documentación de la API se encuentra disponible en la ruta `/docs` una vez que el proyecto esté en marcha.

Si has configurado el fichero `/etc/hosts` como se indica en el README principal, podrás acceder a la documentación de la API en la siguiente URL: [http://library-core.portafolio.loc/docs](http://library-core.portafolio.loc/docs)

## Mensajería

Para la capa de transporte hemos elegido **RabbitMQ**. En `python` existen librerías como `celery` o `kombu` que facilitan la integración con RabbitMQ,
pero para este proyecto hemos optado por usar la librería `pika`, que es una librería de bajo nivel, lo que nos da más control sobre la implementación de la mensajería.

Hemos implementado un Bus InMemory para eventos síncronos y un Messenger InMemory para los asíncronos.

## RabbitMQ - Configuración inicial

En el caso del proyecto que nos ocupa, estamos usando `pika` por tanto la configuración de RabbitMQ es manual.

Siga los siguientes pasos para configurar RabbitMQ:

1. Entra en la interfaz web de RabbitMQ en [http://localhost:15672](http://localhost:15672) con el usuario `guest` y la contraseña `guest`.

2. En la sección de "Exchanges", crea un nuevo exchange con el nombre `library` y el tipo `topic`.

3. En la sección de "Queues", crea una nueva cola con el nombre `library`.

4. En la sección de "Bindings", vincula la cola `library` al exchange `library` con la clave de enrutamiento `app.library`.

## OpenAI - Configuración inicial

En este portafolio nos hemos acoplado a OpenAI, pero se podría implementar una capa de abstracción para poder usar cualquier otro vendor de IA.
Combinando algunos patrones de diseño como factorías, fachadas o estrategias nos podemos desacoplar de un vendor concreto, y así poder cambiarlo en el futuro sin afectar al resto del código.
Pero este no es el caso.

Para configurar OpenAI, sigue los siguientes pasos:

1. En la raiz de esta carpeta deberías de encontrar un fichero `.env`, si lo has copiado siguiendo las instrucciones, si no es el caso, hazlo ahora copiando el fichero `.env.dist` a `.env`.
2. En el fichero `.env` encontrarás la variable `OPENAI_API_KEY`, asigna tu API key de OpenAI a esta variable.

```bash
OPENAI_API_KEY=tu_api_key_aqui
```

3. Guarda el fichero y reinicia los contenedores para que la variable de entorno se cargue correctamente.

```bash
docker compose restart
```

## Gestor de paquetes

En este proyecto estamos usando `uv` como gestor de paquetes, que es una herramienta moderna y ligera para gestionar dependencias en proyectos de Python.
`uv` se encarga de resolver y instalar las dependencias de manera eficiente, y también proporciona un entorno virtual para aislar las dependencias del proyecto.

### Conflicto entre entorno de desarrollo y el contenedor

Si estás desarrollando en tu máquina local y también estás ejecutando el proyecto dentro de un contenedor Docker,
es posible que te encuentres con conflictos entre las dependencias instaladas en tu entorno de desarrollo y las que se encuentran dentro del contenedor.

Para evitar estos conflictos en el contenedor hemos definido la siguiente variable de entorno:

```bash
UV_PROJECT_ENVIRONMENT: /home/${HOST_USER}/.venv
```

Esta variable de entorno le indica a `uv` que use un entorno virtual específico para el proyecto,
lo que ayuda a evitar conflictos entre las dependencias instaladas en tu máquina local y las que se encuentran dentro del contenedor.

Lo unico que debes recordar es asegúrarte de sincronizar los contenedores si instalas nuevas dependencias en tu máquina local.

```bash
docker compose exec core uv sync
docker compose exec worker uv sync
```

## Tests Unitarios

Para ejecutar los tests unitarios, puedes usar el siguiente comando:

```bash
docker compose exec core uv run pytest
```

Y si entras en el container, puedes ejecutar los tests unitarios con los siguientes comandos:

```bash
uv run pytest
```
