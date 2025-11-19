# KnightFight Bot - Dockerfile
FROM python:3.11-bullseye


# Set working directory
WORKDIR /app


# Install system dependencies for Playwright/Chromium
RUN apt-get update && apt-get install -y \
   libnss3 \
   libnspr4 \
   libdbus-1-3 \
   libatk1.0-0 \
   libatk-bridge2.0-0 \
   libcups2 \
   libdrm2 \
   libatspi2.0-0 \
   libx11-6 \
   libxcomposite1 \
   libxdamage1 \
   libxext6 \
   libxfixes3 \
   libxrandr2 \
   libgbm1 \
   libxcb1 \
   libxkbcommon0 \
   libpango-1.0-0 \
   libcairo2 \
   libasound2 \
   libwayland-client0 \
   && rm -rf /var/lib/apt/lists/*


# Copy requirements
COPY bot_highscore_tracker/requirements.txt .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Install Playwright and browsers
RUN playwright install chromium
RUN playwright install-deps chromium


# Copy application code
COPY bot_highscore_tracker/ ./bot_highscore_tracker/


# Create data directories
# RUN mkdir -p bot_data bot_screenshots


# Set environment variables
ENV PYTHONUNBUFFERED=1


# Default command
CMD ["python", "-m", "bot_highscore_tracker.main"]





