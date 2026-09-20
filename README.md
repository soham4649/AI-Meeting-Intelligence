# 🤖 AI Meeting Intelligence

> An NLP-powered web application that transforms unstructured meeting conversations into structured, actionable insights.

## 🌐 Live Demo

🚀 **Live Application:** https://ai-meeting-intelligence-h5vbncdluzehmnncchlklu.streamlit.app/

---

## 📌 Overview

AI Meeting Intelligence analyzes meeting conversations and automatically extracts important information such as:

- 📝 Meeting summary
- 👥 Participants
- ✅ Action items
- 📅 Deadlines
- 💡 Key decisions
- 🎯 Task priorities
- 🧠 Meeting tone
- 📊 Meeting analytics

The goal is to reduce the time required to manually review meeting conversations and identify important tasks and decisions.

---

## ✨ Features

### 📝 Intelligent Meeting Summary
Extracts the most important sentences from a meeting conversation using TF-IDF-based NLP.

### 👥 Participant Detection
Automatically identifies participants from speaker-labelled conversations.

### ✅ Action Item Extraction
Detects tasks assigned during meetings and identifies the responsible person.

### 📅 Deadline Detection
Recognizes deadlines such as:

- Today
- Tomorrow
- Monday–Sunday
- This week
- Next week
- Next month

### 💡 Key Decision Detection
Identifies statements containing decisions, agreements, approvals, and confirmations.

### 🎯 Priority Detection
Detects high-priority tasks using keywords such as:

- Urgent
- ASAP
- Critical
- Immediately
- High priority

### 🧠 Meeting Tone
Provides a basic NLP-based classification of the meeting tone:

- Positive
- Neutral
- Concerned

### 📊 Analytics Dashboard

The dashboard provides:

- Total tasks
- High-priority tasks
- Normal-priority tasks
- Participant workload
- Priority breakdown
- Meeting statistics

### 📄 Transcript Upload

Users can upload a `.txt` meeting transcript instead of manually entering the conversation.

### 📥 Meeting Report

The analyzed meeting can be downloaded as a structured text report.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| Scikit-learn | NLP processing |
| TF-IDF | Text summarization |
| Regular Expressions | Information extraction |
| GitHub | Version control |
| Streamlit Community Cloud | Deployment |

---

## 🔄 How It Works

```text
Meeting Transcript
        ↓
Text Processing
        ↓
Sentence Extraction
        ↓
NLP Analysis
        ↓
┌─────────────────────────┐
│ Summary                 │
│ Participants            │
│ Action Items            │
│ Deadlines               │
│ Key Decisions           │
│ Priority                │
│ Meeting Tone             │
└─────────────────────────┘
        ↓
Analytics Dashboard
        ↓
Downloadable Report
