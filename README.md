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

## sample Execution
#user: Give me certification details of valid_credly user and also give credit score of valid certs.

#system: Certification Details for 'valid-credly-user':

- AWS Certified Solutions Architect – Associate | Issued: 2023-01-01
  | Expires: 2026-01-01 | State: accepted | Active: True | Credit Points: 12

- AWS Certified Cloud Practitioner | Issued: 2024-03-15
  | Expires: 2027-03-15 | State: issued | Active: True | Credit Points: 10

Total Credit Score (Active & Listed in data.json): 22
