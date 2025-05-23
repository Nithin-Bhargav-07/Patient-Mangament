
# How to Run the Hospital Management App

### What you need first

- Python installed (version 3.8 or higher)
- (Optional) A virtual environment to keep things clean

---

### Step 1: Get the project files

Download or clone the project folder to your computer.

---

### Step 2: (Optional) Set up a virtual environment

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install needed packages

Run this command inside the project folder:

```bash
pip install -r requirements.txt
```

---

### Step 4: Create an encryption key

Run this command to make a secret key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the key it shows.

---

### Step 5: Set the key as an environment variable

**On Windows:**

```bash
set FERNET_KEY="paste-your-key-here"
```

**On Mac/Linux:**

```bash
export FERNET_KEY="paste-your-key-here"
```

---

### Step 6: Start the app

Run:

```bash
streamlit run app.py
```

---

### Step 7: Open the app in your browser

Go to the link Streamlit shows (usually http://localhost:8501).

---

### What you can do in the app

- Login as doctor, patient, or other roles
- Add patients and upload their files (PDFs, images)
- Schedule appointments
- See patient and room stats with graphs on the dashboard

---

If you want to deploy this app somewhere online (like Hugging Face Spaces), remember to set the encryption key there too.

---

Let me know if you want me to help with anything else!
