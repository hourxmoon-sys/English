import streamlit as st
from ai_providers import generate_ai_response

def generate_assessment(level: str, skill: str, content_summary: str, provider: str):
    """توليد أسئلة تقييم بناءً على الدرس."""
    prompt = f"""
    أنت معلم لغة إنجليزية. قم بإنشاء 3 أسئلة تقييم قصيرة (اختيار من متعدد) 
    للمستوى {level} لمهارة {skill}.
    ملخص محتوى الدرس: {content_summary}
    قدم الأسئلة باللغة الإنجليزية مع خيارات (A, B, C) وحدد الإجابة الصحيحة في النهاية.
    """
    return generate_ai_response(prompt, provider)

def render_assessment(level: str, skill: str, summary: str, provider: str):
    st.subheader("📝 تقييم الدرس")
    if st.button("توليد أسئلة التقييم", key=f"gen_assess_{level}_{skill}"):
        with st.spinner("جاري توليد الأسئلة..."):
            questions = generate_assessment(level, skill, summary, provider)
            st.session_state[f"assessment_{level}_{skill}"] = questions

    if f"assessment_{level}_{skill}" in st.session_state:
        st.markdown(st.session_state[f"assessment_{level}_{skill}"])
        score = st.slider("ما هو تقييمك الشخصي لأدائك في هذا الدرس؟", 1, 5, 3)
        if st.button("حفظ التقييم", key=f"save_assess_{level}_{skill}"):
            st.success(f"تم حفظ تقييمك ({score}/5). استمر في التقدم!")
