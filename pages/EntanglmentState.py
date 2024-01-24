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

# ################################### Show the Implementation #########################################

st.subheader("Implementation of Entanglement State")
bv_algo_code = """

# ###############Importing libraries###################
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.tools import job_monitor
from qiskit import IBMQ
from random import choice

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

"""


st.code(bv_algo_code, language="python")

st.markdown("""
# Quantum Entanglement Visualization: GHZ and W States

### GHZ State Circuit
The `create_ghz_state` function generates a quantum circuit that prepares the GHZ (Greenberger-Horne-Zeilinger) state for a given number of qubits `n`. The GHZ state is a maximally entangled quantum state.

1. `ghz_circuit = QuantumCircuit(n, n)`: Initialize a quantum circuit with `n` qubits and `n` classical bits for measurement.

2. `ghz_circuit.h(0)`: Apply a Hadamard gate (`H`) to the first qubit (qubit 0). This puts the first qubit into a superposition of |0⟩ and |1⟩ states.

3. Loop through the remaining qubits (qubits 1 to n-1) and apply a controlled-X gate (`CX`) with the first qubit (qubit 0) as the control and each of the other qubits as the target. This entangles all qubits, creating the GHZ state.

4. `ghz_circuit.barrier()`: Insert a barrier in the circuit for visual separation.

5. Measure all qubits and map the measurement results to the classical bits.

6. Return the prepared GHZ state quantum circuit.

### W State Circuit
The `create_w_state` function generates a quantum circuit that prepares the W state for a given number of qubits `n`. The W state is another entangled quantum state.

1. `w_circuit = QuantumCircuit(n, n)`: Initialize a quantum circuit with `n` qubits and `n` classical bits for measurement.

2. `w_circuit.ry(2 * acos(sqrt(1/n)), 0)`: Apply a rotation gate (`RY`) to the first qubit (qubit 0) with an angle determined by the formula `2 * acos(sqrt(1/n))`. This creates a superposition state with unequal amplitudes for |0⟩ and |1⟩.

3. Loop through the remaining qubits (qubits 1 to n-1) and perform the following steps:
   - Apply a controlled-X gate (`CX`) with the previous qubit as the control and the current qubit as the target. This entangles the qubits.
   - Apply another rotation gate (`RY`) to the current qubit with an angle determined by the formula `-2 * acos(sqrt(1/(n - qubit)))`. This adjusts the amplitudes of the superposition, creating the W state.

4. `w_circuit.barrier()`: Insert a barrier in the circuit for visual separation.

5. Measure all qubits and map the measurement results to the classical bits.

6. Return the prepared W state quantum circuit.

### Running the Circuit
The `run_circuit` function is used to execute a given quantum circuit on a specific quantum backend provided by `provider` and collect measurement results.

1. `backend = provider.get_backend(backend_name)`: Retrieve the desired quantum backend (e.g., a quantum simulator or a real quantum device) from the provider.

2. `job = execute(circuit, backend=backend, shots=shots)`: Submit the quantum circuit for execution on the chosen backend with a specified number of measurement shots.

3. `result = job.result()`: Retrieve the result of the executed job.

4. `counts = result.get_counts()`: Extract the measurement outcomes and their corresponding counts.

5. `job_monitor(job)`: Monitor the job's progress (This line is missing an import statement for `job_monitor`).

6. `job.status()`: Check the status of the job.

7. Return the measurement outcomes as counts.

Please note that you may need to import the necessary modules and libraries (e.g., `QuantumCircuit`, `execute`, `job_monitor`, etc.) from a quantum computing framework such as Qiskit to run this code successfully. Additionally, ensure that you have a valid quantum provider and backend set up.
""")

st.markdown("""
For more information on GHZ states and their applications in quantum computing, you can refer to:
* [Qiskit Textbook](https://qiskit.org/textbook)
* [Quantum Computation and Quantum Information by Nielsen and Chuang](https://www.cambridge.org/core/books/quantum-computation-and-quantum-information/32FF2C291D47663B620ACC486C74F926)
""")
# ################################### About the author #########################################
st.subheader("About the Author")

st.image('../images/Gaurang-Belekar.png', caption='Gaurang Belekar',width =200)

# st.sidebar.markdown("""
# Gaurang Belekar is a Quantum Computing enthusiast with a background in Electronics and Communication Engineering. He has experience in Quantum Algorithms, Quantum Machine Learning, and Quantum Cryptography.
# """)

st.write("""
Gaurang Belekar is a Quantum Computing enthusiast with a background in Electronics and Communication Engineering. He has experience in Quantum Algorithms, Quantum Machine Learning, and Quantum Cryptography.
""")


st.write("""   

##### You can connect with him on:
                    
- [GitHub](https://github.com/Gaurang-Belekar)
- [LinkedIn](https://www.linkedin.com/in/gaurang-belekar-ba27171b7/)
""")

