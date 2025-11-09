# Project Tracer — Frontend

This is a minimal React + Vite + Tailwind frontend for the Project Tracer backend.

Quick start (local):

1. From the `project_tracer/frontend` folder install deps:

```powershell
.venv\Scripts\Activate.ps1    # optional: if you use the same venv for Node (not necessary)
npm install
```

2. Run the dev server:

```powershell
npm run dev
```

3. Open http://localhost:5173 and use the UI to POST a Wikipedia URL to the backend at http://127.0.0.1:8003/generate_quiz

Notes:

- Tailwind uses PostCSS; the project includes `tailwind.config.cjs` and `postcss.config.cjs`.
- Deploy to Vercel: push this `frontend` folder to a Git repo and connect the project in Vercel; set the build command `npm run build` and the output directory `dist`.
