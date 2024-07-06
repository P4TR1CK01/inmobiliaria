---------------------------------------------------------------------
          	Hito - Conectando Django a una base de datos
---------------------------------------------------------------------

● Para realizar este desafío debes haber estudiado previamente todo el material
disponible en el LMS correspondiente a la unidad.
● Una vez terminado el desafío, comprime la carpeta que contiene el desarrollo de los
requerimientos solicitados y sube el .zip en el LMS.
● Puntaje total: 10 puntos.
● Desarrollo desafío: Individual o Grupal.

	    Habilidades a evaluar

● Configurar un entorno de desarrollo integrado por Django + PostgreSQL.
● Configurar una aplicación Django para su conexión a una base de datos PostgreSql
utilizando los componentes requeridos.
● Definición y manejo de claves foráneas utilizando el framework Django.
● Implementar operaciones CRUD en los modelos para la manipulación de los datos
acorde al framework Django.

	    Descripción

Una empresa dedicada al arriendo de inmuebles requiere de su ayuda para crear un sitio web
donde usuarios puedan revisar viviendas disponibles para el arriendo. Para esto, la empresa
necesita realizar un diseño de su base de datos que permita almacenar toda su información.

	    Requerimientos

1. Instalación de desarrollo, para esto el ambiente de desarrollo debe contar con las
siguientes características:

	a. Una instalación de PostgreSQL (link)
	b. Creación de un ambiente virtual de Python.
	c. Instalación de los paquetes necesarios para la creación de un proyecto de Django
	d. Una aplicación de Django.
	(3 Puntos)

2. Definición de modelo de datos para representación del problema utilizando el
framework Django:

	a. Representación del modelo relacional de datos.
	b. Conección a la base de datos
	c. Definición y manejo de llaves primarias en columnas foráneas
	(3 Puntos)

3. Implementar operaciones en los modelos para la manipulación de datos utilizando el
framework Django:

	a. Crear un objeto con el modelo.
	b. Enlistar desde el modelo de datos.
	c. Actualizar un registro en el modelo de datos.
	d. Borrar un registro del modelo de datos utilizando un modelo Django.
	(4 Puntos)

      ¡Mucho éxito!

--------------------------------------------------------
            Proyecto - Manejo del CRUD
--------------------------------------------------------

● Para realizar este proyecto debes realizar cada uno de los hitos especificados, así
como revisar todo el material disponible en el LMS correspondiente al módulo.

● Una vez terminado el proyecto completamente, comprime la carpeta que contiene el
desarrollo de los requerimientos solicitados y sube el .zip en el LMS.

● Puntaje total: 10 puntos

● Desarrollo: Individual

            Descripción

El siguiente proyecto constituye una actividad que se desarrollará a lo largo de todo el
siguiente módulo. Para ello, esta se dividirá en los 5 hitos (o partes) siguientes, que
segmentarán los procesos que construirán completamente tu proyecto. Recuerda, por tanto,
que este es un ejercicio acumulativo y que para avanzar al siguiente paso, siempre deberás
contar con el desarrollo del hito que lo antecede. De tal manera, procura siempre avanzar y
corregir aquellos elementos que sean necesarios para completar el siguiente proyecto.

            Contexto

Una empresa dedicada al arriendo de inmuebles requiere de su ayuda para crear un sitio
web donde usuarios puedan revisar inmuebles disponibles para el arriendo, separado por
comuna y región. El sitio web poseerá dos tipos de usuarios: arrendatarios y arrendadores.
Los distintos usuarios deberán poder realizar distintas operaciones dentro del sitio que
serán detalladas a continuación.

            Habilidades a evaluar

	● Identificar fundamentos de la integración del framework Django con bases de 	datos.
	● Crear e integrar un ambiente de trabajo de un proyecto de Django con un modelo de
	datos.
	● Diseñar e implementar interacciones del modelo de datos con vistas de usuarios.

            Descripción

1. Un nuevo usuario se debe poder:
	a. Lograr registrarse en la aplicación.
	b. Actualizar sus datos.
	c. Poder identificarse como arrendatario o como arrendador

Además, un usuario debe tener las siguientes características:
	● Nombres
	● Apellidos
	● RUT
	● Dirección
	● Teléfono personal
	● Correo electrónico
	● Tipo de usuario

2. Un usuario tipo arrendatario debe poder:
	a. Listar las propiedades de diversas propiedades de una comuna específica.
	b. Poder generar una solicitud de arriendo a la propiedad.

Además, el inmueble debe tener las siguientes caracteristicas:
	● Nombre
	● Descripción
	● M2 construidos
	● M2 Totales o del terreno
	● Cantidad de estacionamientos
	● Cantidad de Habitaciones
	● Cantidad de baños
	● Dirección
	● Comuna
	● Tipo de inmueble
		○ Casa
		○ Departamento
		○ Parcela
	● Precio mensual de arriendo

3. Un usuario tipo arrendador debe poder:
	a. Publicar sus propiedades en una comuna determinada con sus características.
	b. Listar propiedades en el dashboard.
	c. Eliminar y editar sus propiedades.
	d. Aceptar arrendatarios.