
# 🧠 Social Media AI Agent Workflow

An end-to-end automated agent workflow for generating social media content, complete with research, content generation, human-in-the-loop feedback, and image synthesis.

Built with [LangGraph](https://github.com/langchain-ai/langgraph), this system intelligently automates content creation from web-sourced data and visualizes the entire process.

---

## 📌 Features

- 🔍 Research Agent: Fetches and reads web pages.
- ✍️ Content Agent: Generates content based on extracted context.
- 🧑‍💻 Human Review: Optional feedback before publication.
- 🎨 Image Agent: Generates accompanying images via instruction-based prompts.
- 🧠 Modular and extensible LangGraph architecture.

---

## 🗂 Project Structure

```bash
.
├── image_agent/        # Handles image generation logic
├── research_agent/     # Handles web scraping and data cleaning
├── social_agent/       # Handles content creation and revisions
├── __init__.py
├── load_model.py       # Model loader and setup
├── langgraph.json      # LangGraph workflow configuration
├── workflow.png        # Visual diagram of the workflow
├── requirements.txt
└── README.md
````

---

## 📊 Workflow Diagram

This diagram illustrates the full LangGraph pipeline:

<p align="center">
  <img src="workflow.png" alt="Workflow Diagram" width="300"/>
</p>

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/bion-slmn/social_media_agent_langgraph.git
cd social_media_agent
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the Workflow

Make sure you're in your virtual environment:

```bash
langgraph dev
```

> This starts the LangGraph development server and runs the workflow defined in `langgraph.json`.

---

## 🛠 Requirements

* Python 3.10+
* [LangGraph](https://pypi.org/project/langgraph/)
* OpenAI-compatible models or your own LLM backends
* Image generation API (e.g., DALL·E, Stable Diffusion)

---

## 🧼 Development Notes

### .gitignore Tips

Make sure `.venv/` and `__pycache__/` are excluded in `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
*.pyo
```

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## 🙋 Contact

Made with ❤️ by [Bion Solomon](https://github.com/bion-slmn)

```



