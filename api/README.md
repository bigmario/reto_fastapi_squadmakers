# Reto Backend - Fast API
## Autor: Mario Castro <mariocastro.pva@gmail.com>

La prueba consiste en crear un API Rest en el framework Fast API utilizando
los siguientes repositorios como base de datos:
<br>
- https://api.chucknorris.io/
- https://icanhazdadjoke.com/api

Crear el API REST con los siguientes endpoints:
<br>
<br>
### ENDPOINT DE CHISTES

- GET: Se devolverá un chiste aleatorio si no se pasa ningún path param.<br>
    - Si se envía el path param habrá que comprobar si tiene el valor “Chuck” o el valor “Dad”
        - Si tiene el valor “Chuck” se conseguirá el chiste de este API https://api.chucknorris.io
        - Si tiene el valor “Dad” se conseguirá del API https://icanhazdadjoke.com/api+
    - En caso de que el valor no sea ninguno de esos dos se devolverá el error correspondiente.

- POST: guardará en una base de datos el chiste (texto pasado por parámetro)

- UPDATE: actualiza el chiste con el nuevo texto sustituyendo al chiste indicado en el parámetro “number”

- DELETE: elimina el chiste indicado en el parametro number.

### ENDPOINT MATEMÁTICO
- GET: Endpoint al que se le pasará un query param llamado “numbers” con una lista de números enteros. La respuesta de este
endpoint debe ser el mínimo común múltiplo de ellos
- GET: Endpoint al que se le pasará un query param llamado “number” con un número entero. La respuesta será ese número + 1.