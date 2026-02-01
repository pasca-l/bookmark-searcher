FROM node:24-bookworm-slim AS builder

# corepack will not be distributed for Node.js 25+
# https://nodejs.org/dist/latest/docs/api/corepack.html
RUN corepack enable && corepack prepare pnpm@10.23.0 --activate

WORKDIR /app
COPY . .

# --force to workaround `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`
RUN pnpm install --force --frozen-lockfile
RUN pnpm run build

FROM nginx:alpine AS server

COPY --from=builder /app/dist /usr/share/nginx/html
