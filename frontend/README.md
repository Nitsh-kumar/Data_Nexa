# DataInsight Frontend

This Vite + React application powers the DataInsight Pro experience. The project
is structured feature-first so that each area (auth, upload, analysis) can grow
independently while sharing common UI primitives.

## Getting Started

```bash
npm install     # install dependencies
npm run dev     # start the local dev server on http://localhost:5173
npm run build   # create a production build
npm run preview # serve the production build locally
```

> ℹ️ If `npm` is unavailable in your environment, install Node.js 18+ from
> https://nodejs.org or use an alternative package manager such as `pnpm`.

## Project Structure

The `src` directory mirrors the architecture shared in the project brief:

- `components/` contains UI primitives (layout, charts, upload widgets, etc.)
- `pages/` hosts route-level components
- `store/` includes Zustand stores for auth, upload, and analysis
- `services/` wraps API calls with Axios
- `hooks/`, `utils/`, and `config/` centralize reusable logic and constants

Refer to the inline comments inside each module for a quick orientation.

