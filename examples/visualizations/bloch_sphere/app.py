import numpy as np
from fasthtml.common import *
import plotly.graph_objects as go
from fh_plotly import plotly2fasthtml, plotly_headers

########################
### FastHTML Section ###
########################

app, rt = fast_app(hdrs=(plotly_headers,))

@rt
def index():
    desc = """
    The Bloch Sphere is a 3D visualization of a single quantum state. 
    You can interact with the buttons (Gates) to see how the state changes. See the description below for more information on what each gate represents.
    """
    hx_vals = 'js:{"gates": document.getElementById("quantum_circuit").textContent}'
    return (Title("Interactive Bloch Sphere"), 
            Main(P(desc),
                 *[Button(gate, hx_get=f"apply_gate/{gate}", hx_target="#chart", hx_swap="innerHTML", hx_vals=hx_vals, title=f"Apply {gate} gate") for gate in single_qubit_gates.keys()], 
                 Button("Reset", hx_get="reset", hx_target="#chart", hx_swap="innerHTML", title="Reset the circuit"),
                 Div(update_state_apply_gate.__wrapped__(), id="chart"),
                 H4("Available gates"),
                 Ul(Li(Strong("H :"),"Hadamard gate. Puts the state in superposition. "),
                    Li(Strong("X :"),"Pauli-X (NOT) gate. Rotate 180 degrees around the X-Axis."),
                    Li(Strong("Y :"),"Pauli-Y (\"bit-flip\") gate. Rotate 180 degrees around the Y-Axis."),
                    Li(Strong("Z :"),"Pauli-Z (\"phase-flip\") gate. Rotate 180 degrees around the Z-Axis."),
                    Li(Strong("S :"),"Phase gate. Rotates around the Z-axis by 90 degrees."),
                    Li(Strong("T :"),"π/8 gate. Rotates around the Z-axis by 45 degrees."))))

@rt
def reset(): return update_state_apply_gate.__wrapped__()

@app.get('/apply_gate/{gate}')
def update_state_apply_gate(gate: str=None, gates: str=None):
    if gates is None: gates = []
    else:
        # Transform from circuit representation to gate names
        gates = [g for g in gates if g in single_qubit_gates.keys()]
        gates.append(gate)
    # Create initial state
    state = np.array([1, 0]) # |0> basis state
    for gate in gates: state = single_qubit_gates[gate] @ state
    # Create visualization
    return Div(plot_bloch(state),
            H4(f"Quantum Circuit: {visualize_circuit(gates)}", id="quantum_circuit"),
            id="chart")

def visualize_circuit(gates: list[str]):
    circuit = "|0⟩-" 
    circuit += "".join([f"[{gate}]─" for gate in gates]) + "|"
    return circuit

############################
### Math/Quantum Section ###
############################


def calculate_coordinates(theta, phi):
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return x, y, z

def create_scenes():
    axis2ticktext = {'X': ['|-⟩', '|+⟩'], 'Y': ['|-i⟩', '|i⟩'], 'Z': ['|1⟩', '|0⟩']}
    scenes = {}
    for axis in ['X','Y','Z']:
        scenes[f'{axis.lower()}axis'] = dict(title=dict(text=axis, font=dict(size=25)), 
                range=[-1.2, 1.2], tickvals=[-1, 1], 
                ticktext=axis2ticktext[axis],
                tickfont=dict(size=15) )
    return scenes

def plot_bloch(state: np.array):
    fig = go.Figure()

    # State vector coordinates
    alpha, beta = state[0], state[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x, y, z = calculate_coordinates(theta, phi)

    # Surface coordinates
    surface_phi, surface_theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
    xs, ys, zs = calculate_coordinates(surface_theta, surface_phi)

    fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.5, colorscale='Blues', showscale=False))

    fig.add_trace(go.Scatter3d(x=[0, x],y=[0, y],z=[0, z], mode='lines+markers+text', marker=dict(size=10, color='green'),
        line=dict(color='green', width=8), textposition="top center", showlegend=True,name=f"{alpha:.2f}|0⟩ + {beta:.2f}|1⟩"))

    # Mark basis states
    fig.add_trace(go.Scatter3d(x=[0, 0, 1, -1, 0, 0],y=[0, 0, 0, 0, 1, -1], z=[1, -1, 0, 0, 0, 0],
        mode='markers', marker=dict(size=5, color='black'), hovertext=['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|i⟩', '|-i⟩'],
        showlegend=False, name="Basis states"))

    # Add lines across axes
    boundary_phi = np.linspace(0, 2 * np.pi, 100)
    coords = [(np.cos(boundary_phi), np.sin(boundary_phi), np.zeros_like(boundary_phi)),
              (np.zeros_like(boundary_phi), np.cos(boundary_phi), np.sin(boundary_phi)),
              (np.cos(boundary_phi), np.zeros_like(boundary_phi), np.sin(boundary_phi)) ]
    
    for x, y, z in coords:
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='black', width=2), showlegend=False, name="Axes"))

    fig.update_layout(scene=dict(**create_scenes(), aspectmode='cube',),
                      legend=dict( font=dict(size=20), x=0.05,y=0.95, xanchor='left', yanchor='top', bgcolor='rgba(0,0,0,0)',),
                      margin=dict(l=0, r=0, t=0, b=0))
    
    return plotly2fasthtml(fig)


single_qubit_gates = {
    # Hadamard
    "H": np.array([[1, 1],
                   [1, -1]]) / np.sqrt(2),
    # Pauli matrices
    "X": np.array([[0, 1],
                   [1, 0]]),
    "Y": np.array([[0, -1j],
                   [1j, 0]]),
    "Z": np.array([[1, 0],
                   [0, -1]]),
    # Phase gates
    "S": np.array([[1, 0],
                   [0, 1j]]),
    "T": np.array([[1, 0],
                   [0, np.exp(1j * np.pi / 4)]])
}




