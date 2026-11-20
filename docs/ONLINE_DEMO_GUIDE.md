# 🌐 Intelligent-AML (C-STGB) — Free Online Lite Demo Publishing Guide

This guide details how to publish and showcase the **Intelligent-AML Web Platform** online on free cloud hosting services for thesis committees, academic examiners, and public demonstrations.

---

## 🏛️ Architecture: Dual-Mode Zero-Cost Deployment

The web platform is engineered with **Dual-Mode Operational Resilience**:

| Mode | Deployment Target | Hosting Cost | What It Runs |
| :--- | :--- | :---: | :--- |
| **Mode 1: Standalone Client Demo** | Vercel, Netlify, GitHub Pages | **$0 / Free Forever** | React 18, WebGL 3D Cytoscape Graph, Real-Time Stream Simulator, 4-Agent SAR Generator, WORM Vault, Scenario Injection |
| **Mode 2: Fullstack Live Microservice** | Hugging Face Spaces, Render, Railway | **$0 / Free Tier** | FastAPI Streaming Backend + DuckDB Arrow Engine + PyTorch Geometric C-STGB Model + React Frontend in a single container |

---

## 🚀 Option 1: Vercel (Recommended — 60-Second Setup)

Vercel provides free, high-speed global CDN hosting with zero server maintenance.

### 1-Click Instant Deploy:
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FNazmulHasanNihal%2FIntelligent-AML&root-directory=frontend)

### Manual Steps / Upgrading Existing Project:
1. Open your project in the [Vercel Dashboard](https://vercel.com/dashboard) → **Settings** → **General**.
2. Under **Root Directory**, click **Edit**, set the path to `frontend`, and click **Save**.
3. Under **Build & Development Settings**, ensure **Framework Preset** is set to **Next.js** (detected automatically) and clear any manual Output Directory overrides.
4. Navigate to **Deployments** → click the `...` menu on the latest commit on `main` → select **Redeploy** (or push any commit to trigger automatic deployment).
5. Within 45-60 seconds, your site is live at `https://intelligent-aml.vercel.app`.

---

## ⚡ Option 2: Netlify (1-Click Free Hosting)

1. Log in to [https://app.netlify.com/](https://app.netlify.com/) with GitHub.
2. Click **Add new site** → **Import an existing project**.
3. Select `Intelligent-AML`.
4. Netlify automatically detects [`netlify.toml`](../netlify.toml):
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
5. Click **Deploy Intelligent-AML**.

---

## 🐙 Option 3: GitHub Pages (100% Free Forever via GitHub Actions)

The repository includes a pre-configured GitHub Actions workflow ([`.github/workflows/deploy-demo.yml`](../.github/workflows/deploy-demo.yml)).

### Activation Steps:
1. In your GitHub repository, navigate to **Settings** → **Pages** (in the left sidebar).
2. Under **Build and deployment** → **Source**, select **`GitHub Actions`**.
3. Push any commit to `main` (or go to the **Actions** tab, select **Deploy Web Demo to GitHub Pages**, and click **Run workflow**).
4. GitHub Actions builds the React application and publishes it to:
   ```
   https://<your-github-username>.github.io/Intelligent-AML/
   ```
5. Client-side deep linking is pre-configured via [`frontend/public/404.html`](../frontend/public/404.html) and [`frontend/index.html`](../frontend/index.html).

---

## 🤗 Option 4: Hugging Face Spaces (Free Fullstack Docker — 16 GB RAM)

Hugging Face Spaces offers **free, persistent cloud compute** (2 vCPUs, 16 GB RAM, 50 GB storage) with a permanent public URL and no credit card required.

### Steps:
1. Go to [https://huggingface.co/new-space](https://huggingface.co/new-space).
2. Set:
   - **Space Name:** `Intelligent-AML`
   - **License:** `MIT`
   - **Space SDK:** Select **`Docker`**
   - **Docker template:** Blank
   - **Space Hardware:** `CPU Basic · 2 vCPU · 16 GB RAM · Free`
3. Push your repository to the Hugging Face Space git remote, or copy [`Dockerfile.demo`](../Dockerfile.demo) as `Dockerfile` in the Space.
4. Hugging Face automatically:
   - Compiles the React 18 frontend assets using Node 20.
   - Installs Python 3.11, PyTorch Geometric, DuckDB, and FastAPI.
   - Launches `uvicorn src.engine.api:app --host 0.0.0.0 --port 7860`.
5. The public live fullstack demo is available at:
   ```
   https://huggingface.co/spaces/<your-username>/Intelligent-AML
   ```

---

## ☁️ Option 5: Render.com (Free Web Service)

1. Sign up at [https://render.com/](https://render.com/) with GitHub.
2. Click **New** → **Blueprint**.
3. Select your repository. Render automatically reads [`render.yaml`](../render.yaml).
4. Click **Apply**.
5. Render deploys the multi-stage Docker container and gives you a free URL (`https://intelligent-aml-demo.onrender.com`).

---

## 🎯 What Reviewers & Committee Members Can Test in the Online Demo

When opening the online demo, all 12 operational consoles are immediately interactive:

1. **Executive Surveillance Desk:**
   - Real-time transaction ingestion feed streaming at realistic bank speed.
   - Live breakdown of Class-Conditional Conformal Risk Triage:
     - **Tier 3 (98.6% STP auto-clear):** Fast-path clean payments.
     - **Tier 2 (0.49% review queue):** Ambiguous cases for Four-Eyes review.
     - **Tier 1 (0.83% auto-hold):** Sanctions and smurfing alerts held in escrow.
2. **Interactive 2D / 3D Forensic Network Studio:**
   - Click nodes and edges to inspect counterparty flow conservation ($\Phi_{\text{flow}}$) and multi-hop layering.
   - Toggle edge-trust camouflage filtering ($\hat{g}_{ij} \ge 0.10$) to prune benign payment chaff.
3. **Scenario Threat Injection:**
   - Click **"Simulate Threat Scenario"** in the top bar to inject:
     - **Scenario A:** MFS Structuring Burst (BDT 99,000 sub-threshold smurfing).
     - **Scenario B:** Corporate Wash-Trading Round-Trip Loop.
     - **Scenario C:** OFAC Sanctioned Entity Instant Containment.
4. **Autonomous 4-Agent SAR/STR Workbench:**
   - View synthesized multi-jurisdictional filings (FinCEN Form 111, BFIU STR-1, UN goAML v4.0).
   - Test AST grammar validation (Proposition 6.1: $\mathcal{V}(\mathcal{T}) \subseteq \mathcal{V}_{\text{sub}}$) guaranteeing 0% hallucination.
   - Click **"Download Dossier"** for instant filing export.
5. **Tamper-Evident Cryptographic WORM Vault:**
   - Verify SHA-256 Merkle tree receipts for court-admissible audit proof under Federal Rules of Evidence FRE 902(11) and SEC Rule 17a-4.
6. **Operator Explainability & Jargon Buster:**
   - Interactive plain-English translation of topological graph signals for non-technical examiners.
