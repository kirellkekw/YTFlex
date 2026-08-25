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

RUN yt-dlp --remote-components ejs:github --skip-download "https://www.youtube.com/watch?v=jNQXAC9IVRw" || true

# Copy only requirements first for caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Now copy the rest of the code (changes frequently)
COPY . ./

# Runs as non-root - /app/mountpoint is a host bind mount (see
# docker-compose.yml), chowned to this same UID on the host side so
# writes (downloads/, the ytflex sqlite db) still work. Deno/yt-dlp above
# stay root-owned under /usr/local - normal, they just need to be
# executable by everyone, not writable.
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set the default command
CMD ["python", "./main.py"]