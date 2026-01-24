


# ================================
# BASE IMAGE
# ================================
FROM python:3.12-slim

# ================================
# SYSTEM PACKAGES
# ================================
RUN apt-get update && \
    apt-get install -y mariadb-server netcat-openbsd python3-venv && \
    rm -rf /var/lib/apt/lists/*

# ================================
# WORKDIR
# ================================
WORKDIR /app

# ================================
# PYTHON VENV
# ================================
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# ================================
# PYTHON DEPENDENCIES
# ================================
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ================================
# APP CODE
# ================================
COPY src ./src

# ================================
# DB INIT SCRIPT
# ================================
COPY init.sql /init.sql
COPY start.sh /start.sh
RUN chmod +x /start.sh

# ================================
# PORTS
# ================================
EXPOSE 8000
EXPOSE 3306

# ================================
# STARTUP
# ================================
CMD ["/start.sh"]


