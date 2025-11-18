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

Assuming you are currently in a WSL terminal and within MySQL workbench you have created a local MySQL connection called 'prizetalk' and within created a database called prizetalk using the command "CREATE DATABASE prizetalk;":

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
   npm install axios
   pip install flask flask-cors bcrypt
   npm install -D tailwindcss postcss autoprefixer
   npm install @heroicons/vue
   ```
4. Run the project:
   ```bash
   cd .. 
   python3 run_all.py
   ```
5. Once you have run the python script called run_all.py it should handle loading all the tables into the local instance of the mysql database and then just click on the link created to access the project, it should say something like this: 'Local:   http://localhost:5173/'.

6. NOTES: with MySQL workbench you may need to go into a local connection and then click on the "Server" in the nav bar, then: Users and Privileges > select root > Login tab > set Host to % (allows all hosts). Then after that restart Workbench.