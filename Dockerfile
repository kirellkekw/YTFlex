FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies first (less likely to change)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Deno JS runtime for yt-dlp's YouTube signature extraction
RUN curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh
ENV PATH="/usr/local/bin:${PATH}"

# Copy only requirements first for caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Now copy the rest of the code (changes frequently)
COPY . ./

# Set the default command
CMD ["python", "./main.py"]