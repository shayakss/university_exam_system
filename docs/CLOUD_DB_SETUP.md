# ☁️ How to Set Up a Free Cloud Database
**For Accessing Your Exam System from Anywhere (Home & Office)**

This guide shows you how to move your database to the cloud using **TiDB Cloud** (Serverless MySQL). This allows you to use the software from any computer with internet access, without needing a VPN.

---

## Step 1: Create a Free Account
1. Go to **[TiDB Cloud](https://tidbcloud.com/free-trial)**.
2. Sign up with Google or Email.
3. Click **"Create Cluster"**.
4. Select **"Serverless"** (This is the Free Forever plan).
5. Give your cluster a name (e.g., `ExamSystemDB`).
6. Choose a region close to you (e.g., Singapore or Mumbai if available, otherwise US West is fine).
7. Click **"Create"**.

---

## Step 2: Get Connection Details
Once your cluster is created (takes ~30 seconds):
1. Click on your cluster name.
2. Click the **"Connect"** button (top right).
3. Select **"Connect with General Client"**.
4. You will see details like this:
   - **Host:** `gateway01.us-west-2.prod.aws.tidbcloud.com`
   - **Port:** `4000`
   - **User:** `2G9s82...`
   - **Password:** (Click "Generate Password")

**⚠️ COPY THESE DETAILS AND KEEP THEM SAFE!**

---

## Step 3: Update `config.json`
On **EVERY PC** (Server and Clients), update your `config.json` file with these new details.

**Open `config.json` and replace the content:**

```json
{
  "use": "mysql",
  "mysql_host": "gateway01.us-west-2.prod.aws.tidbcloud.com",  <-- PASTE HOST HERE
  "mysql_port": 4000,                                         <-- PASTE PORT HERE (Usually 4000)
  "mysql_user": "2G9s82...",                                  <-- PASTE USER HERE
  "mysql_password": "YOUR_GENERATED_PASSWORD",                <-- PASTE PASSWORD HERE
  "mysql_database": "exam_management"
}
```

---

## Step 4: Initialize the Cloud Database
Since this is a brand new database, it's empty. You need to create the tables again.

1. Open your Exam System folder on **ONE PC**.
2. Make sure your `config.json` is saving the Cloud DB details.
3. Run the application (`ExamSystem.exe` or `python main.py`).
4. The system attempts to auto-initialize, but for a clean setup, you might need to run the initialization script if the executable doesn't auto-create tables on first run (our current system *does* check for tables, but let's be sure).

**If you see errors, run this command from the source code folder:**
```cmd
python init_mysql_schema.py
```
*Or if you are using the EXE only, just running it should set up the tables if the database is empty.*

---

## Step 5: Test It!
1. Open the app.
2. Login with default credentials (`admin` / `admin123`).
3. Add a test student.
4. Go to **another computer** (e.g., your home laptop).
5. Use the **SAME `config.json`**.
6. Open the app.
7. You should see the student you added!

---

## ✅ Pros & Cons
| Feature | Local Network (Your specific IP) | Cloud Database (TiDB) |
| :--- | :--- | :--- |
| **Cost** | Free | Free (up to 5GB) |
| **Internet** | Not Required (Works offline in LAN) | **Required** (Must have internet) |
| **Speed** | ⚡ Super Fast | 🐢 Slightly Slower (depends on internet) |
| **Access** | Office Only | **Anywhere** (Home, Office, Cafe) |

**Recommendation:** If you have good internet, **Cloud DB** is much more convenient!
