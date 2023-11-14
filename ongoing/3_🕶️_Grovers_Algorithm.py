# ########### Import Initialisation ############
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.tools import job_monitor
from qiskit import IBMQ
import streamlit as st
import matplotlib.pyplot as plt
from random import choice

# ##############################################


# ############# Grover's Algorithm #############
