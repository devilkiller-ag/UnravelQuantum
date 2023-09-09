import streamlit as st

# Confit
st.set_page_config(page_title='Unravel Quantum', page_icon=":cat:", layout='wide')


st.title("UnravelQuantum")

st.write("""
    UnravelQuantum is your gateway to the world of quantum computing. Discover and explore quantum algorithms with ease, whether you're a newcomer or an experienced researcher. Dive into interactive tutorials, experiment with quantum circuits, and challenge yourself with quizzes. Join a vibrant community of quantum enthusiasts and embark on a quantum journey like never before.
""")


st.subheader("Discover Quantum Algorithm")

st.write("""
    Delve into a comprehensive collection of quantum algorithms meticulously organized from beginner to advanced levels. Each algorithm comes with a wealth of educational resources. Learn about the underlying principles, explore detailed Qiskit Implementation, and or directly run the algorithm without going into the details and code.
""")


st.subheader("About the developer: [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/)")

st.write("""
    [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/) is an engineering physics undergraduate passionate about Quantum Computing, Machine Learning, UI/UX, and Web Development. About two years ago, when he first discovered the field of Web Development and Quantum Computing, it totally amazed him and he have been dedicating his education to them ever since. Over the past two years, he have dedicated a considerable amount of time and effort to learning and developing skills in these fields by taking various online courses, reading different articles, making several projects, and involving in various research internships and mentorship programs. Fast forward to today, He is currently working on a modern streaming platform and researching QUBO Relaxation Parameter Optimisation using Learning Surrogate Solver (QROSS). Explore the below links to explore more about him, his previous projects, blogs, and experience at various organisations.
""")

# ############ Socials ############
c1, c2, c3 = st.columns(3)
with c1:
    st.info('**Portfolio: [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/)**', icon="🔥")
with c2:
    st.info('**GitHub: [@devilkiller-ag](https://github.com/devilkiller-ag)**', icon="😸")
with c3:
    st.info('**GitLab: [@devilkiller-ag](https://gitlab.com/devilkiller-ag)**', icon="🚀")


c4, c5, c6 = st.columns(3)
with c4:
    st.info('**LinkedIn: [jaisarita](https://www.linkedin.com/in/jaisarita/)**', icon="🌐")
with c5:
    st.info('**Twitter: [@jaisarita](https://github.com/devilkiller-ag)**', icon="🐤")
with c6:
    st.info('**Hasnode: [jaisarita](https://jaisarita.hashnode.dev/)**', icon="✍🏻")