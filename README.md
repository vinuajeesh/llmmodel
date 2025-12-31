Complete Windows GGUF Chatbot Application - Development Brief
PROJECT OVERVIEW
Build a production-grade desktop application for Windows that runs local GGUF language models with a modern, polished UI comparable to ChatGPT, Claude Desktop, or Copilot. The application must be robust, user-friendly, and require minimal technical knowledge to operate.

CORE REQUIREMENTS
1. Technology Stack
Backend:

FastAPI (Python 3.12+) with async support

llama-cpp-python for GGUF model loading

duckduckgo-search for web search (v3.8.5+)

SQLite database for persistent storage

uvicorn as ASGI server

Frontend:

React 18+ with TypeScript

Electron for Windows desktop app

TailwindCSS + shadcn/ui for UI components

Zustand for state management

TanStack Query for data fetching

Lucide icons for modern iconography

Packaging:

electron-builder for Windows exe distribution

auto-updater for seamless updates

Architecture:

Backend runs in child process from Electron

IPC communication between frontend and backend

Single-file distribution (.exe installer)

UI/UX REQUIREMENTS
Desktop Application Interface
Design System:

Follow modern design patterns (ChatGPT, Claude Desktop, Copilot)

Dark mode default with light mode toggle

Smooth animations and transitions

Responsive sidebar layout

Professional color palette (blues, purples, grays)

Key Screens:

1. Main Chat Interface
Large message display area with user/assistant distinction

Real-time message streaming with typing indicators

Clear timestamp and model info for each message

Copy message button for each response

Delete/edit message history

Search through chat history

Export conversation as PDF/Markdown

2. Model Management Screen
Model browser/selector (display available GGUF models)

Drag-and-drop model upload area

Model details (file size, parameters, format)

Loading progress with visual indicator

Model swit

