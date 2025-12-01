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

Steps to use the Schema:

1. Go to website: app.eraser.io

2. Click on the "Canvas" tab at the top.

3. On the tool bar to the left, click on the "+" and then click on "Diagram as Code".

4. Click on "Entity Relationship".

5. Once the diagram and code tab pops up, copy and paste the code from the "database_schema_code.txt" and paste it into the coding tab and click of so that it renders.

6. Read the documentation that the website provides on what the code means.

Steps to Export the Schema as an image:

1. Right click on the diagram and then left click on it.

2. Click on "Export Selection".

3. Click the blue "Export" button to download as a PNG.

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

## 🔧 Running Tests

When running tests on new changes to see what is happening in the backend you will need VScode with a a bash terminal and also MySQL workbench.

Within MySQL workbench, you need to have a MySQL connection called 'prizetalk'. Once you are in that connection and you have a query page run these commands:

```sql
CREATE DATABASE prizetalk;
USE prizetalk;
```

Once you have that you now have the database that will store all the tables. You do not need to worry about creating them manually, the python scripts will handle all of that. Just make sure the connector is connected correctly.

Once you connector is set up correctly and you have that databse, run in the terminal:

```bash
python3 run_all.py
```

This file will literally create all the table with extra attributes and load the relevant ones with data. If you need placeholder data to start with you may need to add it manually as needed either through those python files or some other way within MySQL workbench as needed.

Once you have run the script you can click on the localhost link to open the project. Currently the project is set up such that you have two main levels of access. First is the main area with the homepage, signup and login. Once you create and account and login in with it, it will take you to the second area which contains the community page and the global awards page and a sign out button which will take you to the starting area again. 

If you wish to make changes, I recommend first ctrl + c in the terminal to cancel the page. And then do whatever edits you need to do. BUT, before you run the run all script, you must drop ALL the tables from the backend. This can be done by running these commands within MySQL workbench:

```sql
USE prizetalk;
DROP TABLE post_tags_group;
DROP TABLE post_tags;
DROP TABLE reactions_group;
DROP TABLE reactions;
DROP TABLE bookmarks;
DROP TABLE notifications;
DROP TABLE post_reports;
DROP TABLE comment_reviews;
DROP TABLE group_post_comments;
DROP TABLE group_posts;
DROP TABLE group_memberships;
DROP TABLE discussion_groups;
DROP TABLE user_roles;
DROP TABLE post_comments;
DROP TABLE community_posts;
DROP TABLE booker_prize;
DROP TABLE golden_globes;
DROP TABLE grammy;
DROP TABLE nobel_laureates;
DROP TABLE nobel_prizes;
DROP TABLE oscars;
DROP TABLE tags;
DROP TABLE users;
DROP TABLE award_categories;
```

This is EXTREMELY important because I have ran into issues where my program froze and I had to close VScode and MySQL workbench to get it to work again. But this is avoidable as long as you drop the tables before hand so that it starts fresh.

Otherwise it should be good now and run as expected.