

[![CI](https://github.com/aarande/nexradaws/actions/workflows/ci.yml/badge.svg)](https://github.com/aarande/nexradaws/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/aarande/nexradaws/branch/master/graph/badge.svg)](https://codecov.io/gh/aarande/nexradaws) [![Documentation Status](https://readthedocs.org/projects/nexradaws/badge/?version=latest)](http://nexradaws.readthedocs.io/en/latest/?badge=latest) [![Documentation Status](https://readthedocs.org/projects/nexradaws/badge/?version=devel)](http://nexradaws.readthedocs.io/en/devel/?badge=devel)
# nexradaws
Este módulo está diseñado para permitirle consultar y descargar archivos de radar Nexrad desde el almacenamiento S3 de Amazon Web Services. El flujo en tiempo real y el archivo histórico completo de datos NEXRAD en resolución original (Nivel II), desde junio de 1991 hasta la actualidad, ya están disponibles gratuitamente en Amazon S3 para que cualquiera los utilice.
Más información puede encontrarse aquí https://aws.amazon.com/public-datasets/nexrad/.

nexradaws es compatible con Python 3.8+.

Github - https://github.com/aarande/nexradaws

PyPi - https://pypi.python.org/pypi/nexradaws

Documentación - http://nexradaws.readthedocs.io/en/latest/

**Dependencias requeridas**

* boto3
* pytz

**Dependencias opcionales**

* pyart

**Instalación con pip**::

    pip install nexradaws
    pip install nexradaws[pyart] - para instalar con soporte de pyart    

Novedades en la versión 2.0:
* Actualizado para dar soporte a Python 3.8+, se eliminó el soporte para Python 2.7.
* Actualización a los nuevos nombres de bucket para los datos NEXRAD.
* Corrección para NoneType cuando la fecha/hora está en el futuro

Novedades en la versión 1.1:
* Corrección de error para las distintas extensiones de archivo a lo largo de los años (.gz .V06 etc). ¡Gracias a Nick Guy por el PR!
