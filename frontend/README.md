# MindMate Frontend – UI & User Experience Guide

## 📋 Overview

This frontend is the user-facing interface of the **MindMate** application.  
It is designed to provide a clean, friendly, and supportive experience for students.

The frontend includes:
- A dashboard with welcome text and dynamic **Quote of the Day**
- An AI chat interface (Gemini-powered)
- Inspiring placement stories
- Placement tips in clean card layouts
- Fully responsive design
- Ready structure for backend & Firebase integration

---

## 🎯 Frontend Goals

- Keep the UI simple, calm, and student-friendly  
- Avoid overwhelming users with clutter  
- Ensure smooth navigation between pages  
- Make the application feel supportive, not clinical  
- Be fully ready for backend + Firebase integration  

---

## 🗂 Folder Structure

```text
frontend/
├── index.html        # Main dashboard
├── chat.html         # AI chat interface
├── stories.html      # Inspiring placement stories
├── tips.html         # Placement preparation tips
├── styles.css        # Global styles
├── README.md         # Frontend documentation
├── .gitignore        # Git ignore rules

```
---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Any modern web browser (Chrome / Edge / Firefox)
- No build tools required (HTML + CSS + JavaScript)
- Optional: VS Code with Live Server extension

### 2. Run Locally

```bash
cd frontend
```

```# Using Live Server
Right-click index.html → Open with Live Server
```
---
App runs at:
```
http://127.0.0.1:5500/index.html

```
---
🖥 Pages & Features
---
**🏠 index.html – Dashboard**

**Purpose**

- Main landing page for users

**Features**

- App branding (MindMate)

- Welcome banner

- Dynamic Quote of the Day

- Navigation cards:

- Chat Support

- Inspiring Stories

- Placement Tips
---
💬 chat.html – AI Chat Interface
---
**Purpose**

- Allows students to interact with the AI assistant

**Features**

- Message input + send button

- User & AI message bubbles

- Typing animation

- Scrollable chat area

**Backend Ready**

- Sends requests to POST /chat

- Displays AI responses

- Shows warning banner if distress detected
---
🌟 stories.html – Inspiring Stories
---
**Purpose**

- Motivate students using placement journeys

**Features**

- Story cards with:

- Title

- Description

- Company

- Role

- “Show More Stories” button

- Hover animations
---
🎯 tips.html – Placement Tips
---

**Purpose**

- Provide actionable placement preparation advice

**Features**

- Card-based layout

- Icon + title + description

- Clean spacing

- Back to Dashboard button
---
🎨 Styling (styles.css)
---
- Google Font: Poppins

- Soft gradient background

- Rounded cards & subtle shadows

- Hover animations

- Fully responsive layout
---
🧠 Dynamic Quote System
---
- Quotes change based on page:

- Home

- Stories

- Tips

Logic:

- Page detected using window.location.pathname

- One random quote shown per page load
```const quotes = {
  home: [...],
  stories: [...],
  tips: [...]
};
```
---
🔗 Backend Integration
---
- Chat API: POST /chat

- CORS enabled

- Warning UI shown when warning: true

- API URL to be added once backend is deployed

**🔐 Security & Privacy (Frontend)**

- No personal data stored

- Anonymous user IDs

- No API keys in frontend

- HTML escaping used

**📦 Deployment Ready**

Compatible with:
- Firebase Hosting

- GitHub Pages

- Netlify

- Vercel

- ( Firebase Hosting recommended )
---
**👥 Team Contribution**
---
- Member 1 – Frontend & UI

- Designed full UI

- Built dashboard, chat, stories & tips pages

- Implemented responsive design

- Added dynamic quote system

- Prepared frontend for backend & Firebase

- Created frontend README documentation
---
**📝 Next Steps**
---
 - Connect Firestore for stories & tips

-  Replace static quotes with Firestore

 - Add loading skeletons

 - Improve accessibility

 - Add dark mode (optional)
---
**📞 Support**
---
- If UI issues occur:

- Check browser console

- Ensure styles.css is linked

- Verify backend API URL

- Test pages individually
