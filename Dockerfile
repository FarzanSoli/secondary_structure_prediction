# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Install git and curl
RUN apt-get update && \
    apt-get install -y git curl

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt

# Clone the GitHub repository
RUN git clone https://github.com/psipred/s4pred \
    && cd s4pred \
    && curl -O http://bioinfadmin.cs.ucl.ac.uk/downloads/s4pred/weights.tar.gz \
    && tar -xvzf weights.tar.gz \
    && rm weights.tar.gz \
    && touch __init__.py


WORKDIR /app
COPY . /app
COPY psipred_modal_script.py .
ENV DATA_FILE=""
ENV OUTPUT_FILE=""

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug

ENTRYPOINT ["python", "psipred_modal_script.py"]
CMD ["./Input_File.txt", "-o", "./Secondary_structure.fas"]
