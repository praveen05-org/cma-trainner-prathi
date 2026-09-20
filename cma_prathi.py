import streamlit as st
import google.generativeai as genai

# 1. API KEY SETUP
API_KEY = "AQ.Ab8RN6IoxN8QlNMWipUkOkq-Id7-j4YksYmfCmVeWeIR5yWLoQ"
genai.configure(api_key=API_KEY)

# Active Gemini Flash model
model = genai.GenerativeModel('gemini-3.6-flash')

st.set_page_config(page_title="CMA Trainer", page_icon="🎓", layout="wide")

cma_syllabus = {
    "Group 1": {
        "Paper 5: Business Laws and Ethics": "Indian Contract Act, Sale of Goods Act, Corporate Governance, Ethics.",
        "Paper 6: Financial Accounting": "GAAP, Partnership Accounting, Non-Profit Organizations, Accounting Standards.",
        "Paper 7: Direct and Indirect Taxation": "Income Tax Act 1961, Computation of Income, GST Registration & Returns, Customs Duty.",
        "Paper 8: Cost Accounting": "Material & Labour Costing, Standard & Marginal Costing, CVP Analysis."
    },
    "Group 2": {
        "Paper 9: Operations & Strategic Management": "Production Planning, Inventory Management, Business Policy, CSR.",
        "Paper 10: Corporate Accounting and Auditing": "Company Accounts, Auditing Standards, Types of Audits.",
        "Paper 11: Financial Management & Business Data Analytics": "Capital Budgeting, Working Capital, Data Science for Business.",
        "Paper 12: Management Accounting": "Standard Costing, Variance Analysis, Budgetary Control, Decision Theory."
    }
}

st.title("🎓 CMA Trainer - Complete Prep Platform")

menu = st.sidebar.radio("Enna panna virumburinga?", [
    "💬 Ask Doubts (AI Chat)", 
    "📚 Study Materials & Notes", 
    "📝 MCQ Practice", 
    "✍️ Model Exam & AI Correction"
])

# 1. LIVE CHAT FEATURE
if menu == "💬 Ask Doubts (AI Chat)":
    st.header("💬 Ask Any CMA Doubt")
    st.write("CMA syllabus, concepts, formulas pathi entha doubt irundhalum inga type panni ketkalam!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your CMA doubt here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("CMA Trainer alosikidhu..."):
                try:
                    sys_prompt = f"You are CMA Trainer, an expert ICMAI professor and mentor. Answer this student's doubt clearly with simple explanations and practical examples based on ICMAI standards: {prompt}"
                    response = model.generate_content(sys_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")

# 2. STUDY MATERIALS & NOTES
elif menu == "📚 Study Materials & Notes":
    st.header("CMA Intermediate Syllabus 2022")
    group = st.selectbox("Group-a select pannunga:", ["Group 1", "Group 2"])
    
    st.write("---")
    for paper, topics in cma_syllabus[group].items():
        with st.expander(f"📖 {paper}"):
            st.write(f"**Key Topics:** {topics}")
            if st.button(f"Generate Notes for {paper}"):
                with st.spinner("AI Notes uruvakkugirathu..."):
                    try:
                        prompt = f"Act as CMA Trainer, an expert CMA India professor. Give a detailed conceptual summary and exam study tips for {paper} focusing strictly on {topics} based on ICMAI standards."
                        response = model.generate_content(prompt)
                        st.success("Notes Ready!")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")

# 3. MCQ PRACTICE
elif menu == "📝 MCQ Practice":
    st.header("📝 Custom MCQ Generator")
    all_subjects = list(cma_syllabus["Group 1"].keys()) + list(cma_syllabus["Group 2"].keys())
    subject = st.selectbox("Subject-a select pannunga:", all_subjects)
    difficulty = st.select_slider("Difficulty Level:", options=["Easy", "Medium", "Hard", "Exam Level"])
    
    if st.button("Generate 5 MCQs"):
        with st.spinner("Kelvigal thayaraguthu..."):
            try:
                prompt = f"Create 5 multiple choice questions for the CMA India Intermediate exam on the subject: {subject}. Difficulty level: {difficulty}. Give the 5 questions first. Leave some space, then provide the correct answers with detailed conceptual explanations."
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# 4. EXAM EVALUATOR
elif menu == "✍️ Model Exam & AI Correction":
    st.header("✍️ AI Exam Evaluator")
    question = st.text_input("Enter Question:")
    user_answer = st.text_area("Your Answer:", height=200)
    
    if st.button("Submit for AI Correction"):
        if question and user_answer:
            with st.spinner("AI thiruthugirathu..."):
                try:
                    prompt = f"""Act as CMA Trainer, a strict CMA India paper evaluator. 
                    Question: {question}
                    Student Answer: {user_answer}
                    Format: 1. Marks (out of 10), 2. Correct points, 3. Missing keywords, 4. Tips to improve."""
                    response = model.generate_content(prompt)
                    st.success("Correction Completed!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")