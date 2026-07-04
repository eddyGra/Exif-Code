from flask import Flask, render_template, request, jsonify, send_file
import io
from PIL import Image
import piexif

app = Flask(__name__)

# --- LÓGICA DE ESTEGANOGRAFÍA (Ocultar/Revelar) ---

def encode_text_in_image(image, text):
    # Convertir texto a binario y añadir un delimitador de fin de mensaje (####)
    binary_secret = ''.join(format(ord(char), '08b') for char in text + "####")
    
    # Asegurar que la imagen está en modo RGB
    img = image.convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    data_index = 0
    binary_len = len(binary_secret)
    
    for y in range(height):
        for x in range(width):
            if data_index < binary_len:
                r, g, b = pixels[x, y]
                
                # Modificar el bit menos significativo de cada canal
                if data_index < binary_len:
                    r = (r & ~1) | int(binary_secret[data_index])
                    data_index += 1
                if data_index < binary_len:
                    g = (g & ~1) | int(binary_secret[data_index])
                    data_index += 1
                if data_index < binary_len:
                    b = (b & ~1) | int(binary_secret[data_index])
                    data_index += 1
                
                pixels[x, y] = (r, g, b)
            else:
                break
    return img

def decode_text_from_image(image):
    img = image.convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    binary_data = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
            
    # Agrupar en bytes de 8 bits
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    # Convertir bytes a caracteres
    decoded_text = ""
    for byte in all_bytes:
        decoded_text += chr(int(byte, 2))
        if "####" in decoded_text: # Si encontramos el delimitador, paramos
            return decoded_text.replace("####", "")
            
    return "No se encontró ningún mensaje oculto."

# --- RUTAS DE FLASK ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/exif', methods=['POST'])
def view_exif():
    if 'image' not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400
    
    file = request.files['image']
    img_bytes = file.read()
    
    exif_data = {}
    try:
        exif_dict = piexif.load(img_bytes)
        # Extraer metadatos comunes legibles (Cámara, Software, GPS si existen)
        for ifd in ("0th", "Exif", "GPS"):
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                value = exif_dict[ifd][tag]
                if isinstance(value, bytes):
                    value = value.decode('utf-8', errors='ignore')
                exif_data[tag_name] = str(value)
    except Exception:
        return jsonify({"exif": {}, "message": "No se encontraron metadatos EXIF estructurados."})
        
    return jsonify({"exif": exif_data, "message": "Metadatos leídos con éxito." if exif_data else "Imagen limpia de metadatos EXIF."})

@app.route('/api/hide', methods=['POST'])
def hide_message():
    if 'image' not in request.files or 'message' not in request.form:
        return jsonify({"error": "Faltan datos"}), 400
        
    file = request.files['image']
    secret_text = request.form['message']
    
    img = Image.open(file.stream)
    # Esconder el secreto en los píxeles
    stego_img = encode_text_in_image(img, secret_text)
    
    # Guardar el resultado en memoria para enviarlo de vuelta
    img_io = io.BytesIO()
    stego_img.save(img_io, format='PNG') # PNG para que la compresión no destruya los bits ocultos
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='imagen_oculta.png')

@app.route('/api/reveal', methods=['POST'])
def reveal_message():
    if 'image' not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400
        
    file = request.files['image']
    img = Image.open(file.stream)
    
    secret_text = decode_text_from_image(img)
    return jsonify({"message": secret_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)