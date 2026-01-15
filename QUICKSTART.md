# 🚀 Quick Start Guide

## 30-Second Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Backend
```bash
python -m flask run --app app
```
Leave this running in a terminal.

### Step 3: Open Frontend
Simply open `index.html` in your web browser.

---

## That's It! 🎉

Now you can:
1. Drag & drop a CSV file
2. Click the microphone and speak
3. Watch your SQL query get generated

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Cannot connect to API" | Start Flask: `python -m flask run --app app` |
| "Microphone not working" | Browser will ask permission - click "Allow" |
| "No speech detected" | Speak clearly, closer to microphone |
| "ImportError" | Run: `pip install -r requirements.txt` |

---

## Sample CSV Format

Save this as `sample.csv` to test:

```csv
table_name,column_name,description
users,id,Unique user identifier
users,name,User's full name
users,email,User's email address
users,created_at,Account creation date
products,id,Unique product ID
products,name,Product name
products,price,Product price
products,category,Product category
orders,id,Unique order ID
orders,user_id,Reference to user who placed order
orders,product_id,Reference to product ordered
orders,quantity,Number of items ordered
orders,total,Order total price
orders,order_date,Date order was placed
```

---

## Voice Commands Examples

Try saying:
- "Show me all users"
- "Get orders from January"
- "Count total orders per user"
- "Find products in electronics category"
- "What's the average order value"

---

## Browser Requirements

- Chrome 🟢
- Firefox 🟢  
- Edge 🟢
- Safari 🟡 (may need HTTPS)

---

**You're ready to go! 🎤✨**
