FROM node:24-bookworm-slim AS frontend
WORKDIR /app/frontend
RUN npm install --global pnpm@11.25.0
COPY frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm build

FROM python:3.13-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 CC_SERVE_FRONTEND=1
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ backend/
COPY --from=frontend /app/frontend/dist frontend/dist
COPY deploy/start.sh deploy/start.sh
RUN python backend/manage.py collectstatic --noinput && useradd --create-home careconnect
USER careconnect
EXPOSE 10000
CMD ["sh", "deploy/start.sh"]
