
# Subida de Archivos a S3 con Lambda y FastAPI

Este proyecto permite subir archivos a Amazon S3 mediante una API construida con FastAPI y desplegada en AWS Lambda. Los archivos se reciben en formato base64, se validan y se suben a un bucket de S3. Además, se permite especificar la partición (carpeta) en la que se desea almacenar el archivo.

## Requisitos

1. **Python 3.8+**
2. **AWS Account** (con permisos para crear Lambda y S3)
3. **AWS CLI** (si se usa para despliegue)

### Dependencias

```txt
fastapi==0.85.0
boto3==1.24.12
python-multipart==0.0.5
python-magic==0.4.18
pydantic==1.9.0
uvicorn==0.18.3
```

### Instrucciones para Configurar y Desplegar

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/tuusuario/s3-upload-lambda.git
   cd s3-upload-lambda
   ```

2. **Crea un entorno virtual**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Para macOS/Linux
   venv\Scripts\activate      # Para Windows
   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Compila y despliega en AWS Lambda**:

    - Crea un archivo `lambda_function.py` que importe y ejecute tu API FastAPI utilizando `Mangum`, que permite ejecutar FastAPI en AWS Lambda:

      ```python
      from mangum import Mangum
      from app import app
 
      handler = Mangum(app)
      ```

    - **Empaqueta el proyecto para Lambda**:

      Usa la herramienta `Zappa` o cualquier otra solución que prefieras para empaquetar y desplegar el código en Lambda. Ejemplo de comando usando `zappa`:

      ```bash
      zappa deploy dev
      ```

5. **Configura tu Bucket de S3**:

   Asegúrate de tener un bucket de S3 disponible. La configuración del bucket debe incluir las políticas adecuadas de permisos para permitir la carga de archivos.

6. **Prueba el despliegue**:

   Una vez desplegado en AWS Lambda, puedes probar la API con el ejemplo de solicitud `curl`.

---

## Ejemplo de Solicitud `curl`

Aquí tienes un ejemplo de cómo hacer una solicitud `curl` para subir un archivo codificado en base64 a la API de Lambda:

```bash
curl -X POST "https://your-api-endpoint.amazonaws.com/dev/upload" -H "Content-Type: application/json" -d '{
    "file_content": "BASE64_ENCODED_FILE_CONTENT",
    "folder": "myfolder",
    "filename": "example.png"
}'
```

### Parámetros:
- `file_content`: El contenido del archivo codificado en base64. Debes convertir tu archivo a base64 para enviarlo de esta forma.
- `folder`: La partición (o carpeta) dentro de S3 donde deseas almacenar el archivo. Si no se proporciona, el archivo se guardará en la raíz del bucket.
- `filename`: El nombre con el que deseas guardar el archivo en S3.

### Respuesta Esperada:
```json
{
    "message": "File uploaded successfully",
    "s3_path": "myfolder/example.png",
    "s3_url": "https://your-bucket-name.s3.amazonaws.com/myfolder/example.png"
}
```

---

## Seguridad y Consideraciones

- **Permisos de AWS Lambda**: Asegúrate de que tu función Lambda tenga permisos suficientes para interactuar con S3 (política de IAM adecuada).
- **Validación de Archivos**: Actualmente, el sistema permite solo ciertos tipos de archivos no ejecutables (por ejemplo, imágenes, documentos PDF, texto, etc.). Asegúrate de que los tipos de archivo sean validados correctamente antes de proceder con la carga.

---

## Contribuciones

Las contribuciones son bienvenidas. Si tienes alguna mejora o corrección, abre un **Pull Request**.
