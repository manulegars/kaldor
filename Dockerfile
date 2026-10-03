FROM python:3.14.4-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app
RUN groupadd --gid 10001 simulator && useradd --uid 10001 --gid 10001 --no-create-home simulator
COPY --chown=10001:10001 app /app/app
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()"]
CMD ["python", "-m", "app.server"]
