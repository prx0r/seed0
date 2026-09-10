# prx0r/blogengine

sha=7ad36a4259c55024c85cf31bc1ff3cc23cb03aa8

## README excerpt

# Distillery / Blogengine

Next.js app for the Distillery feed, personal diary pages, and the local Elemental Journal.

Live site: https://prx0r.github.io/blogengine/

## Development

```bash
npm install
npm run dev
```

The app uses server routes and Postgres-backed helpers for the live feed/source management flow. Local runtime data expects the relevant environment variables, especially `DATABASE_URL` when API routes touch the database.

## Pages Deployment

GitHub Pages is intentionally configured for **Actions workflow deployment**, not legacy `main/docs` serving.

Important files:

- `.github/workflows/pages.yml` builds and uploads the static artifact with `actions/deploy-pages`.
- `scripts/build.mjs` creates a GitHub Pages static export.
- `next.config.ts` applies `output: "export"`, `basePath: "/blogengine"`, and `assetPrefix: "/blogengine/"` only when `GITHUB_PAGES=true`.
- `.gitignore` ignores generated `docs/` because the workflow uploads it as an artifact.

The app has server-only pieces that cannot be exported directly: `src/app/api`, `src/app/entry`, `src/lib/db.ts`, and `src/middleware.ts`. During `npm run build:pages`, `scripts/build.mjs` temporarily moves those paths into `.static-disabled-for-pages/`, runs `next build`, copies `out/` to `docs/`, writes `.nojekyll`, and restores the moved files in `finally`.

Use this to verify the Pages build locally:

```bash
npm run lint
npm run build:pages
```

If GitHub Pages starts serving stale or errored content again,
