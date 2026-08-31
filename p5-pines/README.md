# INSTALACION Y CONFIGURACION DE LA PRACTICA.
## 1.- Clona el repo:
```
git clone https://github.com/RafaSanav/PWII_Practica2_Schema_inputs_queries_resolvers
cd p5-pines
```
## 2.- Crear el entorno virtual:
```cmd
python -m venv .venv
.venv\Scripts\activate 
```

## 3.- Instalamos dependencias
**Nos aseguramos de tener el entorno virtual activo**
(Debe aparecer (.venv) al inicio de la terminal)
Instalamos los paquetes necesarios con:
```
pip install -r requirementes.txt
```

## 4.- Levantamos el servidor
Iniciamos el servidor con el comando:
```
uvicorn main:app --reload
```

## 5.- Servidor disponible
El servidor estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000). 

Podemos acceder a la interfaz de GraphQL para probar las Queries y Mutations en:
`http://127.0.0.1:8000/graphql`