# ########## Import Initialisation ############
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.tools import job_monitor
from qiskit import IBMQ
import streamlit as st
import matplotlib.pyplot as plt

# #############################################


# ########## Deustch Josza Algorithm ##########
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


def run_on_simulator(provider, backend):
    answer = RunCircuit(dj_circuit, provider, backend, shots=1024)
    st.subheader("Result Counts:")
    st.write(answer)  # Display result counts as text
    st.subheader("Histogram:")
    fig, ax = plt.subplots()  # Create a Matplotlib figure and axes
    plot_histogram(answer, ax=ax)  # Pass the axes to the plot_histogram function
    st.pyplot(fig)  # Display the Matplotlib figure using st.pyplot


def run_on_real_backend(provider_api_key, backend):
    IBMQ.save_account(provider_api_key, overwrite=True)
    provider = IBMQ.load_account()
    # backend = 'ibm_perth'
    answer = RunCircuit(dj_circuit, provider, backend, shots=1024)
    st.subheader("Result Counts:")
    st.write(answer)  # Display result counts as text
    st.subheader("Histogram:")
    fig, ax = plt.subplots()  # Create a Matplotlib figure and axes
    plot_histogram(answer, ax=ax)  # Pass the axes to the plot_histogram function
    st.pyplot(fig)  # Display the Matplotlib figure using st.pyplot


# ########## Use the DJ Algorithm ##########
st.title("Deustch Josza Algorithm")

n = st.slider("Select the number of qubits (n)", 1, 10, 3)
st.write(f"Selected number of qubits: {n}")

f0allx = ConstantFunctionOracale(n, 0)
f1allx = ConstantFunctionOracale(n, 1)
f01half = BalancedFunctionOracle(n, "101", "101")

dj_circuit = DeustchJoszaAlgo(n, f0allx)

providers = {"Basic Aer": BasicAer, "Aer": Aer}
selected_provider = st.selectbox("Select Provider", list(providers.keys()))
backends = providers[selected_provider].backends()
selected_backend = st.selectbox("Select Backend", list(backends))

if st.button("Run on Simulator"):
    if selected_provider in providers:
        run_on_simulator(providers[selected_provider], str(selected_backend))

# provider_api_key = st.text_input("Enter your IBM Quantum Experience API Key (for real backend)")

# if st.button("Run on Real Backend") and provider_api_key:
#     backends = IBMQ.backends()
#     selected_backend = st.selectbox("Select Backend", list(backends))
#     run_on_real_backend(provider_api_key, selected_backend)