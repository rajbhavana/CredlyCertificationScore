# CredlyCertificationScore
This project fetches a Credly user's certifications and calculates a **credit score** based on active certifications that match entries in `data.json`.

It uses:
- **Python**
- **LangChain + LangGraph**
- **Groq LLM (llama-3.3-70b-versatile)**
- **data.json** rules for scoring

---

## 🎯 Features

✅ Fetch all certifications from Credly user profile  
✅ Check certification status (active/expired)  
✅ Validate certificate names using exact match from `data.json`  
✅ Calculate and return a **Total Credit Score**  
✅ Display detailed certification information  

![Architecture Diagram](https://github.com/rajbhavana/CredlyCertificationScore/blob/main/sample%20output.jpeg)

