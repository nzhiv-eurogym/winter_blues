import streamlit as st
from datetime import datetime

st.set_page_config(page_title="How to beat the winter blues", page_icon="❄️", layout="centered")

import base64

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Фон всей страницы */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Основной контейнер с контентом */
        .block-container {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2.5rem;
            border-radius: 18px;
            max-width: 900px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background2.png")


st.markdown("""
<style>
/* 1) Неактивная полоса (серый трек) */
.stSlider [data-baseweb="slider"] [data-baseweb="track"] {
  background: #E6E6E6 !important;
}

/* 2) Активная полоса (заливка) — голубая */
.stSlider [data-baseweb="slider"] [data-baseweb="track"] > div {
  background: #A8D8F0 !important;
}

/* 3) Ползунок (thumb) */
.stSlider [role="slider"] {
  background-color: #A8D8F0 !important;
  border-color: #A8D8F0 !important;
  box-shadow: none !important;
}

/* 4) Hover (чуть насыщеннее) */
.stSlider [role="slider"]:hover {
  background-color: #7EC3E6 !important;
  border-color: #7EC3E6 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("❄️ «Как победить зимнюю хандру» - сборник советов")
st.caption("Ответь на вопросы по шкале 1–5 (1 — ложь, 5 — истина). В конце ты получишь результат и советы.")

QUESTIONS = [
    "Мне все время хочется прилечь.",
    "Мне грустно и тоскливо, когда я осознаю, что новогоднее волшебство закончилось.",
    "Я чувствую раздражение, когда понимаю, что нужно возвращаться в рабочий ритм.",
    "Я бездумно сижу в телефоне, а потом испытываю чувство вины.",
    "Мысль о прогулке в морозную погоду вызывает отвращение.",
    "Новогодние фильмы и украшения больше меня не радуют.",
    "Мне не хочется заниматься или помогать в работе по дому.",
    "Мне кажется, что новый год ничего не изменит в моей жизни и будет таким же, как и прошлый.",
    "После новогодних каникул я не вижу смысла в зиме.",
    "Я НЕ уверен(а), что был честен/честна с самим собой.",
]

SCALE_HELP = "1 — ложь • 2 — скорее ложь • 3 — не знаю/50-50 • 4 — скорее истина • 5 — истина"

# ✅ Инициализация session_state (анонимная история)
if "results_history" not in st.session_state:
    st.session_state.results_history = []


def advice_for_score(total: int) -> tuple[str, str]:
    if 10 <= total <= 19:
        return (
            "🏆 «Ты мой кумир»",
            "- Если хочется согреть душу, то выпей какао с маршмэллоу либо чай с сахаром в термосе из Старкофе и съешь кусочек ароматной пиццы, например, пеперонни.\n- Душа поёт, пой и ты: Last Christmas, Jingle bells\n- Если вздумал ты грустить, то вспомни цитату Эйнштейна: «Есть два способа прожить жизнь: или так, будто чудес не бывает, или так, будто вся жизнь — чудо»",
            "pic1.png"
        )
    elif 20 <= total <= 29:
        return (
            "🌤️ «Держись, все будет хорошо!»",
            "- Совет 1\n- Совет 2\n- Совет 3",
            "pic2.png"
        )
    elif 30 <= total <= 39:
        return (
            "🧣 «Всё не так уж и плохо, как тебе кажется»",
            "- Совет 1\n- Совет 2\n- Совет 3",
            "pic3.png"
        )
    else:  # 40–50
        return (
            "🤍 «Я с тобой!»",
            "- Совет 1\n- Совет 2\n- Совет 3",
        )


def band_for_score(total: int) -> str:
    if 10 <= total <= 19:
        return "10–19"
    if 20 <= total <= 29:
        return "20–29"
    if 30 <= total <= 39:
        return "30–39"
    return "40–50"


# =========================
# Форма
# =========================
with st.form("winter_blues_form"):
    st.subheader("Вопросы")
    st.caption(SCALE_HELP)

    answers = []
    for i, q in enumerate(QUESTIONS, start=1):
        val = st.slider(
            f"{i}. {q}",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            key=f"q{i}",
        )
        answers.append(val)

    submitted = st.form_submit_button("Посчитать результат", key="submit_quiz")


# =========================
# Результат + сохранение в session_state
# =========================
if submitted:
    total = sum(answers)
    honesty = answers[-1]

    title, tips, image_path = advice_for_score(total)

    band = band_for_score(total)

    st.session_state.results_history.append(
        {
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "band": band,
            "title": title,
        }
    )

    st.subheader("Результат")

    st.image(image_path, use_container_width=True)

    st.metric("Твои баллы", total)
    st.markdown(f"### {title}")
    st.markdown("**Советы:**\n" + tips)


    if honesty >= 4:
        st.warning(
            "Похоже, ты сомневаешься, что отвечал(а) честно. "
            "Если хочешь более точный результат — попробуй пройти ещё раз в спокойном состоянии 🙂"
        )

    st.markdown(
        """
**С любовью,  
Лето** ☀️
"""
    )

st.divider()
