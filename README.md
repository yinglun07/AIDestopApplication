# AIDestopApplication

**README
Title + Overview
Setup Instructions
How to Run
Example Usage
Summary**


**Title + Overview**
This project implements a fully local AI-powered desktop application capable of analyzing and querying short video files (~1 minute). The system supports natural language interaction, enabling users to extract insights such as transcription, object detection, and summarized reports.
The application is built with a modular architecture using a Python-based gRPC backend, MCP-inspired agents, and a React + Tauri desktop frontend. All AI inference is performed locally without any cloud dependency.

**Setup Instructions**
**1. Clone repository**

git clone <your-repo-url>
cd AIDestopApplication

**2. Install frontend dependencies**
npm install

**3. Install backend dependencies**
pip install -r requirements.txt

**4. Install Rust (for Tauri)**
curl https://sh.rustup.rs -sSf | sh


**How to Run**
**Development Mode**

**Start frontend:**
npm run dev

**Start backend:**
source venv/bin/activate   
uvicorn main:app --reload

**Start Tauri:**
npx tauri dev

**Production Build**
npm run build   
npx tauri build

**Run the generated desktop application from:**
src-tauri/target/release/


**Example Usage**
**Sample Queries**

1. “Transcribe the video.”
2. “What objects are shown in the video?”
3. “Summarize our discussion so far and generate a PDF.”

**Example Outputs**

1. Transcribed text from video
2. Detected objects and descriptions
3. Generated PDF summary report
4. Example of Human-in-the-loop clarification

**Summary**

The system successfully implements a fully local AI-powered video analysis desktop application. Users can upload .mp4 videos and interact with the system using natural language queries.
The following features are fully functional:
Video transcription using a local speech-to-text model.
Object detection and basic visual understanding using a Vision Agent.
Natural language query routing through a Python-based gRPC backend.
MCP-inspired architecture with a dedicated Vision MCP server.
PDF report generation summarizing video content and interactions.
Chat-based UI built with React and packaged using Tauri for desktop deployment.
Persistent chat history stored locally for session continuity.
Human-in-the-loop clarification for ambiguous queries.

**Limitations:**

1. No PPTX report generation
The system currently supports PDF report generation only. PowerPoint (PPTX) export is not implemented, and report output is limited to document-style summaries.
2. MCP server scope limitation
Only one MCP server (Vision MCP Server) is implemented; other components (transcription and generation) are handled within agent logic rather than separate MCP services.
3. Graph detection is not explicitly implemented and visual analysis is limited to general object detection and scene description.

**Challenges Encountered:**

Adopting new technologies such as gRPC, MCP-style architecture, and Tauri required a learning curve, particularly in understanding inter-process communication and system orchestration across multiple components.

**Potential Improvement:**
1. Introduce additional MCP servers for transcription and report generation to fully modularize the system.
2. Add PPTX generation with automated slide design and visual structuring.
