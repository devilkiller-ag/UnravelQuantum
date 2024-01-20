import streamlit as st
from qiskit import QuantumCircuit, execute, Aer, BasicAer
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.tools import job_monitor
import matplotlib.pyplot as plt
from math import acos, sqrt

# ########## Page Config ############
st.set_page_config(page_title='GHZ and W State Visualization - Quantum Magic', page_icon="🌌", layout='wide')

st.title("Quantum Entanglement Visualization: GHZ and W States")

# ########## GHZ State Circuit ################
def create_ghz_state(n):
    ghz_circuit = QuantumCircuit(n, n)
    ghz_circuit.h(0)
    for qubit in range(1, n):
        ghz_circuit.cx(0, qubit)
    ghz_circuit.barrier()
    for i in range(n):
        ghz_circuit.measure(i, i)
    return ghz_circuit

# ########## W State Circuit ##################
def create_w_state(n):
    w_circuit = QuantumCircuit(n, n)
    w_circuit.ry(2 * acos(sqrt(1/n)), 0)
    for qubit in range(1, n):
        w_circuit.cx(qubit - 1, qubit)
        w_circuit.ry(-2 * acos(sqrt(1/(n - qubit))), qubit)
    w_circuit.barrier()
    for i in range(n):
        w_circuit.measure(i, i)
    return w_circuit

def run_circuit(circuit, provider, backend_name, shots=1024):
    backend = provider.get_backend(backend_name)
    job = execute(circuit, backend=backend, shots=shots)
    result = job.result()
    counts = result.get_counts()
    job_monitor(job)
    job.status()
    return counts

# ########## Streamlit Interface #############
n = st.slider("Select number of qubits", 2, 10, 3)
entanglement_scheme = st.selectbox("Select the entanglement scheme", ["GHZ State", "W State"])

providers = {"Basic Aer": BasicAer, "Aer": Aer}
selected_provider = st.selectbox("Select Provider", list(providers.keys()))
backends = providers[selected_provider].backends()
selected_backend = st.selectbox("Select Backend", [backend.name() for backend in backends])

if st.button("Generate State"):
    if entanglement_scheme == "GHZ State":
        circuit = create_ghz_state(n)
    else:
        circuit = create_w_state(n)

    st.write("**Circuit**")
    fig, ax = plt.subplots()
    circuit_drawer(circuit, output='mpl', ax=ax)  # Display the circuit using Matplotlib
    st.pyplot(fig)  # Show the Matplotlib figure in Streamlit

    counts = run_circuit(circuit, providers[selected_provider], selected_backend)
    st.subheader("Result Counts:")
    st.write(counts)  # Display result counts as text
    st.subheader("Histogram:")
    fig, ax = plt.subplots()  # Create a Matplotlib figure and axes
    plot_histogram(counts, ax=ax)  # Pass the axes to the plot_histogram function
    st.pyplot(fig)  # Display the Matplotlib figure using st.pyplot



st.subheader("Implementation of Bernstein Vazirani Algorithm")

st.write(
    """
Reference:
 - [Bernstein Vazirani Algorithm - Q-munity](https://www.qmunity.tech/tutorials/bernstein-vazirani-algorithm)
"""
)

st.code(bv_algo_code, language="python")

# ################################### About the author #########################################
st.subheader("About the author: [Gaurang Belekar]")

# st.write("""
#     [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/) is an engineering physics undergraduate passionate about Quantum Computing, Machine Learning, UI/UX, and Web Development. I am a student driven by the community and who shares what he has learned. I love to work on real world projects about the topics I learn which can be used by others. To accomplish this I frequently attend hackathons and collaborate with companies to work on real-world projects related to my domains. Feel free to contact me if your company is interested in working on awesome projects in these fields with me. I’m currently building most frequently with: JavaScript/Typescript, C++, and Python.Some of the main frameworks and libraries I frequently use are: React.js,Express.js, Tailwind CSS, ShadCN UI, Qiskit,and Pytorch. Explore the below links to explore more about him, his previous projects, blogs, and experience at various organizations.
# """)

st.write("""
 [Gaurang Belekar] senior at Indian Institute of Infromation Technology Dharwad. Quantum Developer and Researcher.
""")

# ############ Socials ############
# c1, c2, c3 = st.columns(3)
# with c1:
#     st.info('**Portfolio: [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/)**', icon="🔥")
# with c2:
#     st.info('**GitHub: [@devilkiller-ag](https://github.com/devilkiller-ag)**', icon="😸")
# with c3:
#     st.info('**GitLab: [@devilkiller-ag](https://gitlab.com/devilkiller-ag)**', icon="🚀")


# c4, c5, c6 = st.columns(3)
# with c4:
#     st.info('**LinkedIn: [jaisarita](https://www.linkedin.com/in/jaisarita/)**', icon="🌐")
# with c5:
#     st.info('**Twitter: [@jaisarita](https://github.com/devilkiller-ag)**', icon="🐤")
# with c6:
#     st.info('**Hashnode: [jaisarita](https://jaisarita.hashnode.dev/)**', icon="✍🏻")