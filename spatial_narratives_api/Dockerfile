FROM python:3.9

WORKDIR /app

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create and activate the virtual environment
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

CMD [ "python", "app.py" ]