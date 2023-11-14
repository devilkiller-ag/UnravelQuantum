# ########## Import Initialisation ############
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.tools import job_monitor
from qiskit import IBMQ
import streamlit as st
import matplotlib.pyplot as plt
from random import choice

# #############################################


# ########## Bernstien Vazirani Algorithm ##########
def generate_secret_bitstring(n):
    return "".join(choice("01") for _ in range(n))


# Oracle to implement bitstring multiplication with input state
def BVOracle(n, s=""):
    oracle = QuantumCircuit(n + 1)

    s = s if s else generate_secret_bitstring(n)  # the hidden binary string
    # print(s)

    index = n - 1
    for q in s:
        if q == "1":
            oracle.cx(index, n)
        index -= 1

    return oracle


def BernsteinVaziraniAlgo(n, bv_oracle):
    # We need a circuit with n qubits, plus one ancilla qubit
    # Also we need n classical bits to write the output
    bv_circuit = QuantumCircuit(n + 1, n)

    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)

    # Put Ancilla Qubit in state |->
    bv_circuit.x(n)
    bv_circuit.h(n)

    # Apply barrier
    bv_circuit.barrier()

    bv_circuit = bv_circuit.compose(bv_oracle)

    # Apply barrier
    bv_circuit.barrier()

    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)

    # Apply Measurement
    for i in range(n):
        bv_circuit.measure(i, i)

    return bv_circuit


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
st.set_page_config(
    page_title="Bernstein Vazirani Algorithm - Unravel Quantum",
    page_icon="⚔️",
    layout="wide",
)

st.title("Bernstein Vazirani Algorithm")

# n = st.slider("Select the number of qubits (n)", 1, 10, 3)
s = ""  # secret binary string

header = st.columns([1])
header[0].write("**Number of qubits**")

input = st.columns([1])
n = input[0].slider(
    "Select the number of qubits (n)", 1, 10, 3, label_visibility="hidden"
)
st.write(f"Selected number of qubits: {n}")


header2 = st.columns([1])
header2[0].write("**Secret Bitstring**")

input2 = st.columns([1, 1])
radio_choice = input2[0].radio(
        "Secret Bitstring",
        ["Generate Random Secret Bitstring", "Enter Your Own Secret Bitstring Here"],
        label_visibility="hidden",
)

if radio_choice == "Enter Your Own Secret Bitstring Here":
    s = input2[1].text_input(
        label="Create Your Own Secret Bitstring",
        placeholder="Enter Your Own Secret Bitstring Here",
        label_visibility="hidden",
        disabled=(radio_choice == "Generate Random Secret Bitstring"),
    )


s = s if s else generate_secret_bitstring(n)

bv_oracle = BVOracle(n, s)
bv_circuit = BernsteinVaziraniAlgo(n, bv_oracle)

st.write("**Circuit**")
fig, ax = plt.subplots()
circuit_drawer(bv_circuit, output='mpl', ax=ax) # Display the circuit using Matplotlib
st.pyplot(fig) # Show the Matplotlib figure in Streamlit

providers = {"Basic Aer": BasicAer, "Aer": Aer}
selected_provider = st.selectbox("Select Provider", list(providers.keys()))
backends = providers[selected_provider].backends()
selected_backend = st.selectbox("Select Backend", list(backends))

if st.button("Run on Simulator"):
    st.write("Secret Bitstring: ", s)
    if selected_provider in providers:
        run_on_simulator(bv_circuit, providers[selected_provider], str(selected_backend))

# provider_api_key = st.text_input("Enter your IBM Quantum Experience API Key (for real backend)")

# if st.button("Run on Real Backend") and provider_api_key:
#     backends = IBMQ.backends()
#     selected_backend = st.selectbox("Select Backend", list(backends))
#     run_on_real_backend(bv_circuit, provider_api_key, selected_backend)

# ################################### Show the Implementation #########################################
bv_algo_code = """
# Importing libraries
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.tools import job_monitor
from qiskit import IBMQ
from random import choice

def generate_secret_bitstring(n):
    return ''.join(choice('01') for _ in range(n))

# Oracle to implement bitstring multiplication with input state
def BVOracle(n, s=''):
    oracle = QuantumCircuit(n+1)
    
    s = s if s else generate_secret_bitstring(n) # the hidden binary string
    # print(s)
    
    index = n-1
    for q in s:
        if q == '1':
            oracle.cx(index, n)
        index-=1
    
    return oracle

def BernsteinVaziraniAlgo(n, bv_oracle):
    # We need a circuit with n qubits, plus one ancilla qubit
    # Also we need n classical bits to write the output
    bv_circuit = QuantumCircuit(n+1, n)
    
    # Apply Hadamard gates before querying the oracle 
    for i in range(n):
        bv_circuit.h(i)
        
    # Put Ancilla Qubit in state |->
    bv_circuit.x(n)
    bv_circuit.h(n)
    
    # Apply barrier
    bv_circuit.barrier()
    
    bv_circuit = bv_circuit.compose(bv_oracle)

    # Apply barrier
    bv_circuit.barrier()

    # Apply Hadamard gates before querying the oracle 
    for i in range(n):
        bv_circuit.h(i)

    # Apply Measurement
    for i in range(n):
        bv_circuit.measure(i, i)

    return bv_circuit 

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

n = 3 # number of qubits used to represent s

bv_oracle = BVOracle(n, s='110')
bv_circuit = BernsteinVaziraniAlgo(n, bv_oracle)
bv_circuit.draw('mpl')

# Run on the simulator
provider = BasicAer
backend = 'qasm_simulator'
run_on_simulator(bv_circuit, provider, backend, shots=1024)

# Run on the real backend
# provider_api_key = # your provider api key 
backend = 'ibm_perth'
# run_on_real_backend(bv_circuit, provider_api_key, backend, shots=1024)
"""

st.subheader("Implementation of Bernstein Vazirani Algorithm")

st.write(
    """
Reference:
 - [Bernstein Vazirani Algorithm - Q-munity](https://www.qmunity.tech/tutorials/bernstein-vazirani-algorithm)
"""
)

st.code(bv_algo_code, language="python")
