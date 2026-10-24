import streamlit as st
from curriculum import CEFR_CURRICULUM
from ai_providers import generate_ai_response
from flashcard import add_flashcard, render_flashcard_widget
from assessment import render_assessment

# إعداد الصفحة
st.set_page_config(page_title="English AI Tutor", page_icon="🇬🇧", layout="wide")
st.title("🇬🇧 English AI Tutor - معلمك الذكي للإنجليزية")

# الشريط الجانبي: الإعدادات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    provider = st.selectbox("اختر مزود الذكاء الاصطناعي", 
                            ["openai", "deepseek", "claude", "gemini"])
    st.caption("تأكد من إعداد مفاتيح API في متغيرات البيئة.")
    
    level = st.selectbox("اختر مستواك (CEFR)", list(CEFR_CURRICULUM.keys()))
    st.info(CEFR_CURRICULUM[level]["description"])

    st.divider()
    if st.button("🔄 مسح الجلسة"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# التبويبات الرئيسية
tab1, tab2, tab3 = st.tabs(["📚 الدرس", "🃏 البطاقات", "📊 التقدم"])

with tab1:
    st.header(f"درس المستوى {level}")
    skill = st.radio("اختر المهارة", 
                     ["listening", "reading", "writing", "speaking"],
                     horizontal=True,
                     format_func=lambda x: {
                         "listening": "🎧 استماع",
                         "reading": "📖 قراءة",
                         "writing": "✍️ كتابة",
                         "speaking": "🗣️ تحدث"
                     }[x])

    # عرض المحتوى المقترح
    curr = CEFR_CURRICULUM[level]
    st.write(f"**الموضوعات المقترحة:** {', '.join(curr['vocabulary_topics'])}")
    st.write(f"**القواعد:** {', '.join(curr['grammar_topics'])}")

    if st.button("توليد محتوى الدرس بالذكاء الاصطناعي", key="gen_lesson"):
        prompt = f"""
        أنت معلم لغة إنجليزية. قم بإنشاء درس قصير للمستوى {level} 
        يركز على مهارة {skill}.
        استخدم الموضوعات التالية: {', '.join(curr['vocabulary_topics'])}.
        القواعد المستهدفة: {', '.join(curr['grammar_topics'])}.
        قم بتضمين 5 كلمات مفردات جديدة مع معانيها بالعربية.
        قدم الدرس باللغة الإنجليزية مع شرح بالعربية عند الحاجة.
        """
        with st.spinner("جاري توليد الدرس..."):
            lesson_content = generate_ai_response(prompt, provider)
            st.session_state["current_lesson"] = lesson_content
            st.session_state["lesson_summary"] = prompt[:200]  # ملخص للتقييم

    if "current_lesson" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state["current_lesson"])
        st.markdown("---")

        # إضافة كلمات جديدة إلى البطاقات
        st.subheader("➕ إضافة كلمات جديدة إلى البطاقات")
        col1, col2 = st.columns(2)
        with col1:
            front = st.text_input("الكلمة (English)", key="fc_front")
        with col2:
            back = st.text_input("المعنى (Arabic)", key="fc_back")
        if st.button("إضافة البطاقة"):
            if front and back:
                add_flashcard(front, back)
                st.success(f"تمت إضافة '{front}' إلى البطاقات!")
            else:
                st.warning("الرجاء إدخال الكلمة والمعنى.")

        # التقييم
        if "lesson_summary" in st.session_state:
            render_assessment(level, skill, st.session_state["lesson_summary"], provider)

with tab2:
    render_flashcard_widget()

with tab3:
    st.header("📊 لوحة التقدم")
    if "flashcards" in st.session_state and st.session_state.flashcards:
        total = len(st.session_state.flashcards)
        reviewed = sum(1 for fc in st.session_state.flashcards if fc["review_count"] > 0)
        st.metric("إجمالي البطاقات", total)
        st.metric("البطاقات التي تمت مراجعتها", reviewed)
        st.progress(reviewed / total if total > 0 else 0)
    else:
        st.info("لا توجد بيانات تقدم بعد. ابدأ بإضافة بطاقات!")
