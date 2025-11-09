Frontend deployment and configuration

This frontend is built with Vite + React and expects the backend API base URL in a Vite env variable named `VITE_API_BASE`.

1) Local development
- Start the frontend locally (defaults to localhost backend if VITE_API_BASE not set):

```powershell
cd project_tracer/frontend
npm install
npm run dev
```

2) Configure backend URL for production
- If your backend is at `https://jhansi-six.vercel.app/` set the environment variable in Vercel (or your hosting provider) as:
  - Key: `VITE_API_BASE`
  - Value: `https://jhansi-six.vercel.app`

3) Deploy to Vercel (recommended quick flow)
- From the project root (where `package.json` lives), run:

```powershell
cd project_tracer/frontend
vercel --prod
```

- Or use the Vercel dashboard: New Project → Import Git Repository → select this frontend folder.
- In the Vercel project settings, add the Environment Variable `VITE_API_BASE` (Production) with value `https://jhansi-six.vercel.app`.

4) Notes
- Vite only exposes env vars that start with `VITE_` to the client bundle.
- Do not commit secrets into your repo. Keep `.env` files in `.gitignore`.
- If backend uses a path other than `/history` or `/generate_quiz`, update `src/App.jsx` accordingly.

If you want, I can set the Vercel environment variable for you (I can give the exact CLI commands to run locally).