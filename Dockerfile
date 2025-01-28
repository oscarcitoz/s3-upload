# Imagen base oficial de Python
FROM public.ecr.aws/lambda/python:3.9

# Copiar archivos
COPY app.py lambda_handler.py .
COPY requirements.txt .

# Instalar dependencias
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Configurar el handler para Lambda
CMD ["lambda_handler.handler"]