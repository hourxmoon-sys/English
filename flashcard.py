import streamlit as st
from sm_2 import Scheduler, Card
import datetime

# --- بداية التهيئة الآمنة ---
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
# --- نهاية التهيئة الآمنة ---

def add_flashcard(front: str, back: str):
    """إضافة بطاقة جديدة إلى النظام."""
    card = Card()
    st.session_state.flashcards.append({
        "front": front,
        "back": back,
        "card_obj": card,
        "due": card.due,
        "review_count": 0
    })

def review_flashcard(index: int, rating: int):
    """تقييم البطاقة وتحديث موعد المراجعة."""
    fc = st.session_state.flashcards[index]
    card, _ = st.session_state.scheduler.review_card(fc["card_obj"], rating)
    fc["card_obj"] = card
    fc["due"] = card.due
    fc["review_count"] += 1

def get_due_flashcards():
    """إرجاع البطاقات المستحقة للمراجعة الآن."""
    now = datetime.datetime.now(datetime.timezone.utc)
    due_cards = []
    for i, fc in enumerate(st.session_state.flashcards):
        due = fc["due"]
        if isinstance(due, str):
            due = datetime.datetime.fromisoformat(due)
        if due <= now:
            due_cards.append((i, fc))
    return due_cards

def render_flashcard_widget():
    """واجهة مستخدم لعرض البطاقات ومراجعتها."""
    st.subheader("🃏 البطاقات التعليمية (Flashcards)")
    if not st.session_state.flashcards:
        st.info("لا توجد بطاقات بعد. أضف كلمات جديدة أثناء الدروس.")
        return

    due = get_due_flashcards()
    if not due:
        st.success("لا توجد بطاقات مستحقة للمراجعة الآن. عمل رائع!")
        return

    for idx, fc in due:
        with st.expander(f"🔹 {fc['front']}", expanded=False):
            st.markdown(f"**الإجابة:** {fc['back']}")
            st.caption(f"تمت المراجعة {fc['review_count']} مرة.")
            col1, col2, col3, col4 = st.columns(4)
            if col1.button("❌ نسيت", key=f"rate0_{idx}"):
                review_flashcard(idx, 0)
                st.rerun()
            if col2.button("😕 صعب", key=f"rate2_{idx}"):
                review_flashcard(idx, 2)
                st.rerun()
            if col3.button("👍 جيد", key=f"rate3_{idx}"):
                review_flashcard(idx, 3)
                st.rerun()
            if col4.button("🌟 ممتاز", key=f"rate5_{idx}"):
                review_flashcard(idx, 5)
                st.rerun()
