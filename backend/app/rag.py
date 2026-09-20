import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import MODEL_NAME, DATA_DIR
from .models import Job, Course

class RAGIndex:
    """Grounded retrieval: documents are chunked before embedding and indexed in FAISS."""
    def __init__(self, model, items: list[dict], text_fn, chunk_size=420, chunk_overlap=60):
        self.model=model; self.items=items
        splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.chunks=[]
        for item in items:
            text=text_fn(item)
            for chunk in splitter.split_text(text):
                self.chunks.append({"item":item,"text":chunk})
        texts=[c["text"] for c in self.chunks]
        vectors=model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        self.vectors=np.asarray(vectors,dtype="float32")
        self.index=faiss.IndexFlatIP(self.vectors.shape[1]); self.index.add(self.vectors)

    def search(self, query: str, k=8):
        q=self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)
        scores,ids=self.index.search(np.asarray(q,dtype="float32"), min(k,len(self.chunks)))
        best={}
        for rank,i in enumerate(ids[0]):
            if i<0: continue
            item=self.chunks[i]["item"]
            key=item["id"]
            score=float(scores[0][rank])
            if key not in best or score>best[key]["score"]:
                best[key]={"item":item,"score":score,"chunk":self.chunks[i]["text"]}
        return list(best.values())

class KnowledgeBase:
    def __init__(self):
        self.model=SentenceTransformer(MODEL_NAME)
        jobs=json.loads((DATA_DIR/"jobs.json").read_text(encoding="utf-8"))
        courses=json.loads((DATA_DIR/"courses.json").read_text(encoding="utf-8"))
        self.jobs=[Job(**x) for x in jobs]; self.courses=[Course(**x) for x in courses]
        self.job_index=RAGIndex(self.model,jobs,lambda x: f"JOB {x['id']} | {x['title']} | {x['company']} | {x['location']} | Required: {', '.join(x['required_skills'])} | Preferred: {', '.join(x['preferred_skills'])} | {x['description']}")
        self.course_index=RAGIndex(self.model,courses,lambda x: f"COURSE {x['id']} | {x['title']} | Provider: {x['provider']} | Skills: {', '.join(x['skills'])} | Level: {x['level']} | Duration: {x['duration_weeks']} weeks | Cost: INR {x['cost']}")

    def search_jobs(self, query, location, k=8):
        hits=self.job_index.search(query,k=30)
        loc=location.lower().strip()
        if loc:
            local=[h for h in hits if h["item"].get("location","").lower()==loc]
            if local: hits=local
        return hits[:k]

    def search_courses(self, skill, free_only=False, k=5):
        hits=self.course_index.search(skill,k=20)
        out=[]
        for h in hits:
            item=h["item"]
            if free_only and item.get("cost",0)!=0: continue
            out.append(h)
        return out[:k]

    def job_by_id(self, job_id):
        return next((j for j in self.jobs if j.id==job_id),None)
