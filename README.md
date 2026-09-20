# SkillPath AI — C4 Skill-Gap-to-Job Matching Agent

A hackathon-ready implementation of the C4 problem: turn a candidate profile into local job matches, grounded skill gaps, opportunity-driven course recommendations, and a measurable time-to-ready roadmap.

## What is implemented

- 40 curated/demo job records across multiple Indian locations
- 60 curated/demo training records with duration, cost and skill metadata
- PDF resume ingestion with deterministic skill extraction
- Profile skill normalization
- RAG pipeline: loaders → recursive text splitter → Sentence Transformer embeddings → FAISS vector store → retriever
- LangGraph multi-step orchestration
- Decorated Python tools for normalization, job scoring, opportunity counting and time/cost calculation
- Source/evidence chunks returned to the UI
- Free-only training mode
- Opportunity-driven ranking: missing skill → local jobs requiring that skill
- “What if I learn this?” simulation
- Interactive React dashboard with job explorer, agent trace and roadmap
- Loading, error, empty and responsive states

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The first start downloads the Sentence Transformer model if it is not cached.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown by the terminal.

Optional API URL:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

## Demo flow

1. Start with the prefilled B.Tech/backend profile or upload a PDF resume.
2. Choose a target location.
3. Run analysis.
4. Show the agent trace.
5. Open the top opportunity and inspect the skill matrix.
6. Show the opportunity-driven skill cards.
7. Click **What if I learn…?** to demonstrate a deterministic re-score.
8. Open the roadmap to show sequential weeks and total cost.

## Important data note

The included job/course records are curated demo data for the hackathon prototype. Replace course URLs and job records with verified sources before production use. The UI intentionally labels the data as curated rather than implying live employment availability.


## Deployment

### Backend — Render
1. Push the repository to GitHub.
2. Create a Render Web Service with root directory `backend`, build command `pip install -r requirements.txt`, and start command `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3. Set `CORS_ORIGINS` to the final Vercel URL.
4. Verify `/api/health` before connecting the frontend.

### Frontend — Vercel
1. Import the same repository and set root directory to `frontend`.
2. Build with `npm run build`; output is `dist`.
3. Set `VITE_API_URL` to the Render backend URL.

The included `render.yaml` and `frontend/vercel.json` provide the deployment defaults.
