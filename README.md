# 🖼 Exif-Code

Herramienta web para extraer y analizar metadatos **EXIF** de imágenes. Construida con Python y Flask, con interfaz de estética terminal/hacker.


---

## ¿Qué hace?

Sube una imagen y obtén al instante:

- 📍 **Coordenadas GPS** con enlace directo a Google Maps
- 📷 **Datos de la cámara** — modelo, fabricante, lente
- 📅 **Fecha y hora** en que fue tomada la foto
- 🖥 **Software** con el que fue editada
- 📐 **Resolución y dimensiones**
- 🔢 **Todos los tags EXIF** embebidos en el archivo

> ⚠️ Muchas fotos tomadas con smartphone contienen coordenadas GPS sin que el usuario lo sepa. Esta herramienta lo hace visible.

---

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/eddyGra/Exif-Code.git
cd Exif-Code

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

Abre tu navegador en: **`http://localhost:5000`**

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3 | Backend |
| Flask | Servidor web |
| Pillow | Extracción de EXIF |
| HTML / CSS / JS | Frontend (sin frameworks) |

---

## Estructura

```
Exif-Code/
├── app.py              # Backend Flask + lógica de extracción
├── templates/
│   └── index.html      # Interfaz web
└── requirements.txt    # Dependencias
```

## Autor

**Eduardo** —
[GitHub](https://github.com/eddyGra)

---

> Desarrollado con fines educativos y de uso ético. Úsalo responsablemente.# no.name
