# ########## Import Initialisation ############
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.tools import job_monitor
from qiskit import IBMQ
import streamlit as st
import matplotlib.pyplot as plt
from random import choice
# #############################################


# ########## Deustch Josza Algorithm ##########
def generate_bitstring(n):
    return "".join(choice("01") for _ in range(n))

def ConstantFunctionOracale(n, output):
    oracle = QuantumCircuit(n + 1)  # n input qubits, 1 ancillia qubit for |->
    if output == 0:
        return oracle
    elif output == 1:
        # Performing X on all qubits except one qubit(k) is computationally same as performing X only on one qubit(k)
        oracle.x(n)
        return oracle
    else:
        return "Error: Invalid function output"

def BalancedFunctionOracle(n):
    xGatesString = cxGatesString = generate_bitstring(n)
    if len(xGatesString) != n:
        return "Error: Invalid length of X Gate String"
    if len(cxGatesString) != n:
        return "Error: Invalid length of CX Gate String"

    oracle = QuantumCircuit(n + 1)  # n input qubits, 1 ancillia qubit for |->

    # Place X-gates before implementing CX gates in the next loop
    for i in range(n):
        if xGatesString[i] == "1":
            oracle.x(i)

    # Place CX-gates to give phase at desired combinations
    for m in range(n):
        if cxGatesString[m] == "1":
            oracle.cx(m, n)

    # Place X-gates again to revert to original inputs on 0 to n-1 qubits
    for k in range(n):
        if xGatesString[k] == "1":
            oracle.x(k)

    return oracle


def DeustchJoszaAlgo(n, FunctionOracle):
    dj_circuit = QuantumCircuit(n + 1, n)

    # Apply H-gates
    for qubit in range(n):
        dj_circuit.h(qubit)

    # Put ancilia qubit in state |->
    dj_circuit.x(n)
    dj_circuit.h(n)

    dj_circuit.barrier()

    # Add Oracle
    dj_circuit = dj_circuit.compose(FunctionOracle)

    dj_circuit.barrier()

    # Repeat H-Gates
    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.barrier()

    # Measure
    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit


def RunCircuit(circuit, provider, backend_name, shots=1024):
    backend = provider.get_backend(backend_name)
    job = execute(circuit, backend=backend, shots=shots)
    results = job.result()
    counts = results.get_counts()
    job_monitor(job)
    job.status()
    return counts


def run_on_simulator(circuit, provider, backend):
    answer = RunCircuit(circuit, provider, backend, shots=1024)
    st.subheader("Result Counts:")
    st.write(answer)  # Display result counts as text
    st.subheader("Histogram:")
    fig, ax = plt.subplots()  # Create a Matplotlib figure and axes
    plot_histogram(answer, ax=ax)  # Pass the axes to the plot_histogram function
    st.pyplot(fig)  # Display the Matplotlib figure using st.pyplot


def run_on_real_backend(circuit, provider_api_key, backend):
    IBMQ.save_account(provider_api_key, overwrite=True)
    provider = IBMQ.load_account()
    # backend = 'ibm_perth'
    answer = RunCircuit(circuit, provider, backend, shots=1024)
    st.subheader("Result Counts:")
    st.write(answer)  # Display result counts as text
    st.subheader("Histogram:")
    fig, ax = plt.subplots()  # Create a Matplotlib figure and axes
    plot_histogram(answer, ax=ax)  # Pass the axes to the plot_histogram function
    st.pyplot(fig)  # Display the Matplotlib figure using st.pyplot


# ########## Use the DJ Algorithm ##########

# Page Config
st.set_page_config(page_title='Deustch Josza Algorithm - Unravel Quantum', page_icon="⚔️", layout='wide')

st.title("Deustch Josza Algorithm")

n = st.slider("Select the number of qubits (n)", 1, 10, 3)
st.write(f"Selected number of qubits: {n}")

f0allx = ConstantFunctionOracale(n, 0)
f1allx = ConstantFunctionOracale(n, 1)
f01half = BalancedFunctionOracle(n)

functions = {"Constant Function (f(x) = 0)": f0allx, "Constant Function (f(x) = 1)": f1allx, "Balanced Function": f01half}
selected_function = st.selectbox("Select the type of function", list(functions.keys()))

dj_circuit = DeustchJoszaAlgo(n, functions[selected_function])

st.write("**Circuit**")
fig, ax = plt.subplots()
circuit_drawer(dj_circuit, output='mpl', ax=ax) # Display the circuit using Matplotlib
st.pyplot(fig) # Show the Matplotlib figure in Streamlit

providers = {"Basic Aer": BasicAer, "Aer": Aer}
selected_provider = st.selectbox("Select Provider", list(providers.keys()))
backends = providers[selected_provider].backends()
selected_backend = st.selectbox("Select Backend", list(backends))

if st.button("Run on Simulator") and selected_provider in providers:
    run_on_simulator(dj_circuit, providers[selected_provider], str(selected_backend))

# provider_api_key = st.text_input("Enter your IBM Quantum Experience API Key (for real backend)")

# if st.button("Run on Real Backend") and provider_api_key:
#     backends = IBMQ.backends()
#     selected_backend = st.selectbox("Select Backend", list(backends))
#     run_on_real_backend(dj_circuit, provider_api_key, selected_backend)


# ################################### Show the Implementation #########################################
dj_algo_code = '''
def ConstantFunctionOracale(n, output):
    oracle = QuantumCircuit(n + 1)  # n input qubits, 1 ancillia qubit for |->
    if output == 0:
        return oracle
    elif output == 1:
        # Performing X on all qubits except one qubit(k) is computationally same as performing X only on one qubit(k)
        oracle.x(n)
        return oracle
    else:
        return "Error: Invalid function output"


def BalancedFunctionOracle(n, xGatesString, cxGatesString):
    if len(xGatesString) != n:
        return "Error: Invalid length of X Gate String"
    if len(cxGatesString) != n:
        return "Error: Invalid length of CX Gate String"

    oracle = QuantumCircuit(n + 1)  # n input qubits, 1 ancillia qubit for |->

    # Place X-gates before implementing CX gates in the next loop
    for i in range(n):
        if xGatesString[i] == "1":
            oracle.x(i)

    # Place CX-gates to give phase at desired combinations
    for m in range(n):
        if cxGatesString[m] == "1":
            oracle.cx(m, n)

    # Place X-gates again to revert to original inputs on 0 to n-1 qubits
    for k in range(n):
        if xGatesString[k] == "1":
            oracle.x(k)

    return oracle


def DeustchJoszaAlgo(n, FunctionOracle):
    dj_circuit = QuantumCircuit(n + 1, n)

    # Apply H-gates
    for qubit in range(n):
        dj_circuit.h(qubit)

    # Put ancilia qubit in state |->
    dj_circuit.x(n)
    dj_circuit.h(n)

    dj_circuit.barrier()

    # Add Oracle
    dj_circuit = dj_circuit.compose(FunctionOracle)

    dj_circuit.barrier()

    # Repeat H-Gates
    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.barrier()

    # Measure
    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit


def RunCircuit(circuit, provider, backend_name, shots=1024):
    backend = provider.get_backend(backend_name)
    job = execute(circuit, backend=backend, shots=shots)
    results = job.result()
    counts = results.get_counts()
    job_monitor(job)
    job.status()
    return counts


def run_on_simulator(circuit, provider, backend, shots=1024):
    answer = RunCircuit(circuit, provider, backend, shots)
    plot_histogram(answer)
    return answer


def run_on_real_backend(circuit, provider_api_key, backend, shots=1024):
    IBMQ.save_account(provider_api_key, overwrite=True)
    provider = IBMQ.load_account()
    answer = RunCircuit(circuit, provider, backend, shots)
    plot_histogram(answer)
    return answer

# Create DJ Circuit
f0allx = ConstantFunctionOracale(n, 0)
f1allx = ConstantFunctionOracale(n, 1)
f01half = BalancedFunctionOracle(n, "101", "101")

dj_circuit = DeustchJoszaAlgo(n, f01half)
dj_circuit.draw('mpl')

# Run on the simulator
provider = BasicAer
backend = 'qasm_simulator'
run_on_simulator(dj_circuit, provider, backend, shots=1024)

# Run on the real backend
# provider_api_key = # your provider api key 
backend = 'ibm_perth'
# run_on_real_backend(dj_circuit, provider_api_key, backend, shots=1024)
'''

st.subheader("Implementation of Deustch Jasza Algorithm")

st.write("""
Reference:
 - [Deustch Jasza Algorithm - Qiskit Textbook](https://learn.qiskit.org/course/ch-algorithms/deutsch-jozsa-algorithm)
 - [Deustch Jasza Algorithm - Classiq](https://www.classiq.io/insights/the-deutsch-jozsa-algorithm-explained)
""")

st.code(dj_algo_code, language='python')

# ################################### About the author #########################################
st.subheader("About the author: [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/)")

st.write("""
    [Ashmit JaiSarita Gupta](https://jaisarita.vercel.app/) is an engineering physics undergraduate passionate about Quantum Computing, Machine Learning, UI/UX, and Web Development. I am a student driven by the community and who shares what he has learned. I love to work on real world projects about the topics I learn which can be used by others. To accomplish this I frequently attend hackathons and collaborate with companies to work on real-world projects related to my domains. Feel free to contact me if your company is interested in working on awesome projects in these fields with me. I’m currently building most frequently with: JavaScript/Typescript, C++, and Python.Some of the main frameworks and libraries I frequently use are: React.js,Express.js, Tailwind CSS, ShadCN UI, Qiskit,and Pytorch. Explore the below links to explore more about him, his previous projects, blogs, and experience at various organizations.
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
    st.info('**Hashnode: [jaisarita](https://jaisarita.hashnode.dev/)**', icon="✍🏻")