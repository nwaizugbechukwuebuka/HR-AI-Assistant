# HR-AI-Assistant

An AI-powered **HR Knowledge and Workflow Assistant** designed to provide grounded, context-aware answers from internal HR documentation using **Retrieval-Augmented Generation (RAG)**.

The project combines document processing, semantic search, vector embeddings, and an LLM-based response layer to reduce unsupported answers and ensure that responses are grounded in the organization's HR knowledge base.

---

## Project Overview

HR teams often work with information distributed across employee handbooks, leave policies, onboarding documentation, benefits, codes of conduct, and remote-work policies.

The HR-AI-Assistant provides a centralized interface for retrieving this information through natural-language questions.

### Core RAG Pipeline

```text
HR Documents
     │
     ▼
PDF Document Extraction
     │
     ▼
Text Cleaning & Normalization
     │
     ▼
Document Chunking
     │
     ▼
Sentence Embeddings
     │
     ▼
FAISS Vector Index
     │
     ▼
Semantic Retrieval
     │
     ▼
Relevant Context
     │
     ▼
LLM / RAG Response Generation
     │
     ▼
Grounded HR Answer
```

---

## Current HR Knowledge Base

The current knowledge base contains six HR documents:

1. `employee_handbook.pdf`
2. `leave_policy.pdf`
3. `onboarding_guide.pdf`
4. `code_of_conduct.pdf`
5. `employee_benefits.pdf`
6. `remote_work_policy.pdf`

These documents form the initial source corpus for semantic retrieval.

---

## Key Objectives

* Build a production-oriented AI HR assistant.
* Implement semantic retrieval over internal HR documents.
* Use RAG to ground generated answers in retrieved documentation.
* Provide a clean FastAPI backend.
* Separate document ingestion from retrieval and generation.
* Create a testable and maintainable architecture.
* Support future authentication, authorization, database, frontend, Docker, and CI/CD integration.
* Demonstrate practical experience with AI engineering, backend development, information retrieval, QA, and automation.

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

## AI / RAG

* Sentence Transformers
* `all-MiniLM-L6-v2`
* FAISS
* PyPDF
* Retrieval-Augmented Generation (RAG)
* LLM integration

## Frontend

Planned:

* React
* TypeScript
* Modern component-based UI

## Database

Planned:

* PostgreSQL

## Authentication & Authorization

Planned:

* JWT authentication
* Role-Based Access Control (RBAC)

## DevOps

Planned:

* Docker
* GitHub Actions
* CI/CD

---

# Repository Structure

```text
HR-AI-Assistant/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       ├── ai/
│       ├── ingestion/
│       └── utils/
│
├── frontend/
│
├── data/
│   ├── employee_handbook.pdf
│   ├── leave_policy.pdf
│   ├── onboarding_guide.pdf
│   ├── code_of_conduct.pdf
│   ├── employee_benefits.pdf
│   └── remote_work_policy.pdf
│
├── vector_store/
│   ├── index.faiss
│   └── metadata.json
│
├── scripts/
│   └── ingest_documents.py
│
├── docs/
│
├── screenshots/
│
├── .github/
│   └── workflows/
│
├── requirements.txt
├── README.md
└── .gitignore
```

> The exact directory contents may evolve as additional RAG and application components are implemented.

---

# RAG Architecture

## 1. Document Ingestion

The ingestion pipeline loads the six HR PDF documents and extracts their textual content.

```text
PDF
 ↓
PyPDF
 ↓
Extracted Text
```

The extracted text is then prepared for downstream processing.

---

## 2. Text Processing

Extracted content is cleaned and divided into smaller chunks.

Chunking allows the retrieval system to identify the specific sections of a document that are relevant to a user's question.

```text
Document
   ↓
Clean Text
   ↓
Chunks
   ↓
Metadata
```

---

## 3. Embedding Generation

Each text chunk is converted into a numerical vector using Sentence Transformers.

Current embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings allow semantically similar questions and document passages to be compared.

---

## 4. Vector Storage

The generated embeddings are stored in a FAISS vector index.

```text
Text Chunks
     ↓
Embeddings
     ↓
FAISS
     ↓
index.faiss
```

Associated metadata is stored separately so that retrieved vectors can be mapped back to their original document and chunk.

```text
vector_store/
├── index.faiss
└── metadata.json
```

---

# Semantic Retrieval

The retrieval system converts a user's question into an embedding and searches the FAISS index for semantically similar document chunks.

Example:

```text
User:
"What is the company's annual leave policy?"

        ↓

Question Embedding

        ↓

FAISS Semantic Search

        ↓

Relevant leave-policy chunks

        ↓

Retrieved Context

        ↓

RAG Response
```

This approach allows the system to retrieve relevant information even when the user's wording differs from the wording used in the source document.

---

# Grounded Generation

After retrieving relevant document chunks, the system can provide those chunks as context to an LLM.

```text
User Question
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant HR Context
      │
      ▼
Prompt Construction
      │
      ▼
LLM
      │
      ▼
Grounded Answer
```

The objective is to make the model answer using retrieved organizational information rather than relying solely on its pretrained knowledge.

---

# Backend API

The FastAPI application provides the foundation for the backend service.

Development endpoints include:

```text
GET /
GET /health
GET /docs
```

FastAPI automatically provides interactive API documentation through:

```text
/docs
```

Once the retrieval service is connected to the API, a question endpoint can expose the RAG pipeline to the frontend.

Planned conceptual endpoint:

```text
POST /api/v1/chat
```

Example request:

```json
{
  "question": "How many days of annual leave are available?"
}
```

Example response structure:

```json
{
  "answer": "Retrieved answer from the HR knowledge base.",
  "sources": [
    {
      "document": "leave_policy.pdf"
    }
  ]
}
```

---

# Local Development

## 1. Clone the Repository

```powershell
git clone https://github.com/nwaizugbechukwuebuka/HR-AI-Assistant.git
cd HR-AI-Assistant
```

---

## 2. Create the Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

Core RAG dependencies include:

```text
pypdf
sentence-transformers
faiss-cpu
```

If necessary:

```powershell
python -m pip install pypdf sentence-transformers faiss-cpu
```

---

## 4. Verify RAG Dependencies

```powershell
python -c "import pypdf, sentence_transformers, faiss; print('RAG dependencies OK')"
```

Expected output:

```text
RAG dependencies OK
```

---

# Document Ingestion

Run the ingestion script:

```powershell
python scripts\ingest_documents.py
```

The pipeline is:

```text
PDF documents
      ↓
Text extraction
      ↓
Text cleaning
      ↓
Chunking
      ↓
Embeddings
      ↓
FAISS index
      ↓
Metadata
```

The generated vector store should contain:

```text
vector_store/
├── index.faiss
└── metadata.json
```

---

# Testing Semantic Retrieval

Before connecting the retriever to the chat API, semantic retrieval should be tested directly against the six HR documents.

Example test questions:

```text
1. What does the employee handbook say about workplace expectations?

2. How does the annual leave policy work?

3. What should a new employee do during onboarding?

4. What are the company's rules of conduct?

5. What employee benefits are available?

6. What is the remote work policy?
```

The expected retrieval behavior is:

```text
Question
   ↓
Embedding
   ↓
FAISS Search
   ↓
Top-k Results
   ↓
Relevant HR Document
```

This stage should be validated before connecting retrieval to the conversational API.

---

# Example Retrieval Test

A retrieval test should display information similar to:

```text
Query:
What is the annual leave policy?

Top Results:

1. leave_policy.pdf
   Similarity: <score>

2. employee_handbook.pdf
   Similarity: <score>

3. employee_benefits.pdf
   Similarity: <score>
```

The exact similarity values depend on the embedding model and indexed content.

---

# Development Roadmap

## Phase 1 — Backend Foundation

* [x] Create project structure
* [x] Create FastAPI application
* [x] Add configuration structure
* [x] Add initial API endpoints
* [ ] Complete database integration
* [ ] Implement authentication
* [ ] Implement authorization

---

## Phase 2 — RAG Pipeline

* [x] Collect HR documents
* [x] Add six-document knowledge base
* [x] Add PDF extraction
* [x] Add text processing
* [x] Add Sentence Transformer embeddings
* [x] Add FAISS vector storage
* [ ] Validate semantic retrieval
* [ ] Connect retriever to RAG service
* [ ] Connect RAG service to chat API
* [ ] Add source attribution

---

## Phase 3 — Frontend

* [ ] Create React application
* [ ] Create chat interface
* [ ] Connect frontend to FastAPI
* [ ] Display retrieved sources
* [ ] Add loading/error states
* [ ] Add conversation history

---

## Phase 4 — Security

* [ ] Implement JWT authentication
* [ ] Implement RBAC
* [ ] Protect API endpoints
* [ ] Validate uploaded documents
* [ ] Secure environment variables
* [ ] Add input validation
* [ ] Add logging and audit events

---

## Phase 5 — Testing

* [ ] Unit tests
* [ ] Retrieval tests
* [ ] API tests
* [ ] RAG pipeline tests
* [ ] Integration tests
* [ ] Frontend tests
* [ ] Security tests

---

## Phase 6 — Containerization & CI/CD

* [ ] Create Dockerfile
* [ ] Create Docker Compose configuration
* [ ] Containerize backend
* [ ] Containerize frontend
* [ ] Configure CI pipeline
* [ ] Add automated tests
* [ ] Add deployment pipeline

---

# Quality and Reliability

The project is designed around several engineering principles.

### Grounded Responses

Answers should be based on retrieved HR documentation whenever relevant information exists in the knowledge base.

### Separation of Concerns

Document ingestion, embedding generation, retrieval, API logic, and response generation remain separate components.

### Reproducibility

The same document corpus should produce a reproducible vector index when processed with the same configuration.

### Testability

Individual components should be testable independently before being combined into the complete application.

### Security

The final application should protect HR information through authentication, authorization, input validation, secure configuration, and appropriate logging.

---

# Engineering Focus

The HR-AI-Assistant is not only an AI application. It is designed as an **engineering system** in which retrieval accuracy, backend reliability, software quality, security, and automation are treated as first-class concerns.

The project therefore connects:

```text
AI / RAG
   │
   ├── Semantic Retrieval
   ├── Document Processing
   └── Grounded Generation
          │
          ▼
Backend Engineering
   │
   ├── Python
   ├── FastAPI
   └── API Architecture
          │
          ▼
Software Quality
   │
   ├── Testing
   ├── Validation
   ├── Reliability
   └── CI/CD
          │
          ▼
Security Engineering
   │
   ├── Authentication
   ├── Authorization
   ├── Input Validation
   └── Secure System Design
```

This engineering approach supports the broader objective of building **secure, reliable, testable, and automation-ready software systems**.

---

# Project Status

**Current Version:** `0.1.0`

**Current focus:**

```text
HR Documents
      ↓
PDF Extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
FAISS
      ↓
Semantic Retrieval
      ↓
Retrieval Validation
      ↓
RAG Integration
```

The immediate engineering objective is to **validate real semantic retrieval against the six HR documents before connecting the retriever to the chat API**.

---

# Future Extensions

Potential future capabilities include:

* Conversational HR assistant
* HR administrator dashboard
* Document upload and indexing
* Document version management
* Source citations
* Conversation history
* Employee-specific access controls
* HR analytics
* Audit logging
* Feedback-based retrieval evaluation
* Retrieval quality metrics
* Automated document re-indexing
* Production deployment

---

# About the Developer

### **Chukwuebuka Tobiloba Nwaizugbe**

Aspiring **Security Engineering & QA Automation Professional**

The HR-AI-Assistant reflects this broader engineering focus by combining **AI-assisted information retrieval, backend engineering, software quality, automation, security, and reliable system design**.

**Core Focus:**

* Software Quality Engineering
* Test Automation & CI/CD Systems
* Secure & Reliable System Design
* Backend Engineering (Python ecosystems)

---

<div align="center">

### 🚦 Built for Enterprise QA & Real-World Engineering Systems

**Bridging Software Quality, Automation, AI Engineering, and System Reliability**

[![GitHub](https://img.shields.io/badge/GitHub-Project-181717.svg?style=flat\&logo=github)](https://github.com/nwaizugbechukwuebuka/QA-Defect-Tracking-System)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077b5.svg?style=flat\&logo=linkedin)](https://www.linkedin.com/in/chukwuebuka-tobiloba-nwaizugbe/)
[![Discord](https://img.shields.io/badge/Join%20us%20on-Discord-5865F2?logo=discord\&logoColor=white\&style=for-the-badge)](https://discord.gg/deepworksociety)

</div>
