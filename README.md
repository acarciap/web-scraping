# web-scraping
scraping de información económica

## Descripción:
Hace el “rasgado” del sitio  https://datosmacro.expansion.com para extraer información diversas páginas, y construyen do un dataset que podría ser interesante para entender el nivel de vida de los distintos países del mundo, y cómo ha sido su evolución en el tiempo. 

La extracción ha sido implementada en el lenguaje Python 3.6, y considera diversos aspectos relacionados a las restricciones y especificaciones que pudiera anunciar el propietario del site.

## Autor: 
Antonio Carcia

## Resultados:
### Directorio ./csv
**myData.csv**

## Organización de Fuentes:
### Directorio ./src: 
Incluye el fuente de los objetos desarrollados en código Python 3.6.3 para la implementación del requerimiento, y consta de los siguientes módulos:

**main.py**
Ejecución de la secuencia que permite la construcción del Resultado.

**xDownLoad.py**
Implementa la clase para la descarga de la página. Aplica las restricciones de especificadas en el archivo robots.txt

**xThrottle01.py**
Implementa la clase que da soporte a la aplicación del control necesario para evitar la saturación del servidor. En lugar de 
considerar el instante de acceso de cada página, considera el último acceso al site (es decir, cualquiera de sus páginas)

**Xsmi01.py**
Clase que extrae información relacionada al Salario Mínimo Interprofesional

**Xsm01.py**
Clase que extrae información relacionada al Salario Medio

**Xpib01.py**
Clase que extrae información del PIB

### Directorio ./doc
Incluye los archivos **“acarcia_TD_PRA1.doc”** y **“Apuntes de Trabajo.doc”**, el primero contentivo de las respuestas a la práctica; mientras que el segundo, ofrece un resumen muy específico de aspectos de interés que facilitan la comprensión del trabajo desarrollado, y permite al lector asumir una base sólida para la adopción o mejora de la propuesta sugerida.


## Recursos:
1.	Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
2.	Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC
