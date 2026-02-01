# Bookmark Searcher
Retrieves bookmarked webpages from user query. Works like a personal search engine, where the sources are collected and selected by the user.

## Screenshots

## Requirements
- Docker 27.3.1
- Docker Compose v2.29.7

## Usage
1. Prepare the necessary environmental variables.
- `JWT_SECRET_KEY`
  - can be any string, or generated via `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- `GOOGLE_CLIENT_ID`
  - create a [OAuth2.0 client in Google Cloud](https://console.cloud.google.com/auth/clients), and set `http://localhost:5173` as the "Authorized JavaScript origins".
  - use the "Client ID" displayed at "Additional information".

2. Start application using Docker.
```shell
$ docker compose up
```
> Otherwise open locally using the `make` command. (This requires additional dependencies of [`uv`](https://docs.astral.sh/uv/) and [`pnpm`](https://pnpm.io/).)
> ```shell
> $ make run-local
> ```

3. Open website (port set to 5173).
```
http://localhost:5173
```
