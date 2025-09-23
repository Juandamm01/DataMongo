# Proyecto: Visualización de Aspirantes Unillanos  

Este proyecto es una aplicación web construida con **Flask** que permite:  
1. Mostrar los datos de aspirantes almacenados en una base de datos **MongoDB**.  
2. Generar gráficos a partir de los datos (ejemplo: cantidad de aspirantes por país).  

---

## Requisitos  

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes componentes:  

- **Python 3.8+**  
- **MongoDB** en ejecución local (`mongodb://localhost:27017/`)  
- Librerías necesarias:  

```bash
pip install flask pymongo pandas matplotlib
