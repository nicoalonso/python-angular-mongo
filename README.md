# Portafolio

Este proyecto es un portafolio usando las siguientes tecnologías:

- Python con el Framework FastAPI para el backend
- Angular como frontal
- MongoDB como BD
- RabbitMQ como capa de transporte
- Docker para desarrollo en local
- Arquitectura Hexagonal

# Descripción y casos de uso

Este portafolio se basa en una aplicación de biblioteca, con un catálogo de libros, clientes y proveedores.

Entidades que forman parte de esta aplicación:
- Libro: entidad principal, se podrá adquirir, prestar o comprar un libro.
- Autor: cada libro tiene un autor, y cada autor puede tener varios libros.
- Editorial: cada libro tiene una editorial, y cada editorial puede tener varios libros.
- Cliente: puede solicitar un préstamo de un libro, o comprar un libro.
- Proveedor: puede suministrar libros a la biblioteca.

Casos de Uso:
1. Un cliente puede solicitar un préstamo de un libro, siempre y cuando el libro esté disponible. Tendrá un plazo de devolución de 14 días. Si el libro no se devuelve a tiempo, se le aplicará una multa.
2. Un cliente puede comprar un libro, siempre y cuando el libro esté disponible. El cliente pagará el precio del libro.
3. Un libro estará disponible para ser prestado cuando haya al menos una copia disponible en la biblioteca.
4. Un libro estará disponible para ser comprado cuando este habilitado para la venta, que haya como mínimo 3 libros en stock, y haya al menos una copia disponible en la biblioteca.
5. Un proveedor puede suministrar libros a la biblioteca, aumentando el stock de un libro.
6. Inventario: cuando se adquiera o venda un libro, se lanzará un evento de inventario que actualizará el stock del libro en la biblioteca.
7. A las 12:00 am de cada día, se ejecutará un proceso que revisará los préstamos vencidos y aplicará las multas correspondientes a los clientes.
   (el cron que lanzará este proceso se ha omitido por simplicidad, pero se podría implementar usando un contenedor adicional.

Caso de Uso con IA:

Aprovechando que nos encontramos en python, he decidido implementar un caso de uso donde intervenga la inteligencia artificial.
He elegido como vendor OpenAI por ser el más usado y conocido, para poder probarlo vete a la sección de OpenAI para ver como configurar la API key.

1. Generación de descripciones de libros usando URL como por ejemplo Wikipedia.
2. Generación de biografía de autores usando URL como por ejemplo Wikipedia.

Otros casos de uso:
1. Cuando se da de alta un cliente, se le asociará un número de membresía, que se generará automáticamente. Cada número de membresía es único y se compone de un prefijo "SN" seguido de un número secuencial de 5 dígitos (ejemplo: SN00001, SN00002, etc.). No se puede modificar el número de membresía una vez asignado.

## Get Started

### Clonar repositorio

```bash
git clone <this repo> .
```

### Actualizar el fichero `/etc/hosts`

Mejorar la experiencia de desarrollo en local añadiendo las siguientes líneas al fichero `/etc/hosts`:
Si usas Windows, el fichero se encuentra en `C:\Windows\System32\drivers\etc\hosts`

```bash
# Portafolio library
127.0.0.1 library-core.portafolio.loc
127.0.0.1 library.portafolio.loc
```

### Copiar y modificar el fichero `.env`

Copia el fichero de distribución `.env.dist` a `.env` en caso de que no exista. En las carpetas `core` y `editor` también encontrarás un fichero `.env.dist`, haz lo mismo en cada una de ellas.

```bash
cp .env.dist .env
```

Revisa y modifica las variables que hacen referencia al identificador de usuario y grupo.
Están al principio del fichero. Estas variables son importantes, ya que se usan para compilar las imágenes de docker.
Si son incorrectas tendrías que borrar tanto los contendores como las imágenes y volver a construirlas.

Ejecuta el siguiente comando para comprobar cuál es tu usuario y el grupo con sus correspondientes identificadores.
```bash
id
```

Ejemplo: `uid=100(nico) gid=1000(nico)`

### Crear la carpeta data para los volúmenes de Docker

Para evitar perdida de datos, el contenedor de MongoDB usará un volumen que se montará en la carpeta `data` del proyecto. Es importante crear esta carpeta antes de levantar los contenedores, para evitar problemas de permisos.

```bashbash 
mkdir -p data/mongo/db
mkdir -p data/mongo/config
```

### Levantar los contenedores

Levantamos el proyecto con el comando.
El modificador `-d` detach es opcional.

```bash
docker compose up -d
```

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

4. En la sección de "Bindings", vincula la cola `library` al exchange `library` con la clave de enrutamiento `library`.

## OpenAI - Configuración inicial

En este portafolio nos hemos acoplado a OpenAI, pero se podría implementar una capa de abstracción para poder usar cualquier otro vendor de IA.
Combinando algunos patrones de diseño como factorías, fachadas o estrategias nos podemos desacoplar de un vendor concreto, y así poder cambiarlo en el futuro sin afectar al resto del código.
Pero este no es el caso.

Para configurar OpenAI, sigue los siguientes pasos:

1. En la carpeta `core` deberías de encontrar un fichero `.env`, si lo has copiado siguiendo las instrucciones, si no es el caso, hazlo ahora copiando el fichero `.env.dist` a `.env`.
2. En el fichero `.env` encontrarás la variable `OPENAI_API_KEY`, asigna tu API key de OpenAI a esta variable.

```bash
OPENAI_API_KEY=tu_api_key_aqui
```

3. Guarda el fichero y reinicia los contenedores para que la variable de entorno se cargue correctamente.

```bash
docker compose restart
```
