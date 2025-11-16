# 🏆 PrizeTalk

PrizeTalk is a web platform for exploring **winners of major global awards** such as Nobel, Oscars, Grammys, etc., and discussing their achievements. Within the app, it centralizes the award winner datasets into one place, allowing users to learn, analyze, and engage in community discussions.

---

## 👤 Meet the Team

- Yuriy Slyvka
- Reem Lamsettef
- Dominic Hoiseth

---

## 📚 Features

- **Global Awards Search**
- **Community Page**
- **User Profiles**
- **Analytics Page**

---

## 📂 Datasets Used and Available Awards

- **Nobel Prize** (Peace, Literature, Physics, Physiology/Medicine, Chemistry, Economics)
- **Oscars Award** (Academy Awards winners & nominees)
- **Grammy Award** (Music winners & nominees)
- **Booker Prize** (Literary Winners)
- **Golden Globes Award** (film & TV winners)

---

## 🛠️ Tech Stack

- **Frontend:** Vue.js (UI for browsing, discussions, logins, etc.)
- **Backend:** Python / Flask (data ingestion)
- **Database:** MySQL (relational schema for awards, winners, users, discussions)
- **Data Processing:** Pandas

---

## 🗄️ Database Schema and Other Info

TBD

---

## Prerequisites

### Windows
- Node.js - [direct download link](https://nodejs.org/dist/v22.20.0/node-v22.20.0-x64.msi) (run the installer)

### Linux
```bash
# Node.js
sudo apt update
sudo apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

---

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone <link>
   ```
2. Navigate to the project directory:
   ```bash
   cd PrizeTalk/PrizeTalk_Code
   ```
3. Install dependencies:
   ```bash
   npm install
   npm install vue-router@4
   ```
4. Run the project:
   ```bash
   npm run dev
   ```
5. After running `npm run dev`, copy the localhost link (e.g., `Local: http://localhost:5173/`) and paste it into your preferred browser.