import numpy as np
import cv2
from shapes import create_cylinder, create_from_img
from plotting import plot
import streamlit as st

plot_every = 35

def create_feq(rho, ux, uy, weights, cxs, cys, NL, f_shape):
    Feq = np.zeros(f_shape) 
    for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
        Feq[:, :, i] = rho * w * (1 
            + 3 * (cx * ux + cy * uy) 
            + 9/2 * (cx * ux + cy * uy)**2 
            - 3/2 * (ux**2 + uy**2))
    return Feq

def calc_curl(ux, uy):
    # Calculate the curl
    dfydx = ux[2:, 1:-1] - ux[:-2, 1:-1]
    dfxdy = uy[1:-1, 2:] - uy[1:-1, :-2]
    curl = dfydx - dfxdy

    # Pad the curl array to match the shape of ux and uy
    curl = np.pad(curl, ((1, 1), (1, 1)), mode='constant', constant_values=0)
    return curl

def main():
    # STREAMLIT SETTINGS
    st.title("Lattice Boltzmann Method")
    st.write("This is a simulation of fluid movement")
    shape_select = st.selectbox("Select a shape", ["Circle", "Bullet", "Cow"])
    

    # Check for plot placeholder
    if 'plot_placeholder' not in st.session_state:
        st.session_state.plot_placeholder = st.empty()

    # Check for source
    source = st.checkbox("Add source", value=False)

    source_strength_placeholder = st.empty()
    num_sources_placeholder = st.empty()

    if source:
        source_strength = st.slider("Source strength", 0.0, 5.0, 2.5, step=0.1)
        num_sources = st.slider("Number of sources", 1, 10, 3)
    else:
        source_strength_placeholder.empty()
        num_sources_placeholder.empty()
        source_strength = 0
        num_sources = 1
        st.session_state['plot_placeholder'].empty()

    # Check for wind
    wind = st.checkbox("Add wind", value=False)

    wind_speed_placeholder = st.empty()
    wind_dir_placeholder = st.empty()

    if wind:
        wind_speed = wind_speed_placeholder.slider("Wind speed", 0.0, 1.0, 0.1, step=0.1)
        wind_dir = wind_dir_placeholder.slider("Wind direction", 0.0, 2*np.pi, np.pi/4, step=np.pi/4)
    else:
        wind_speed_placeholder.empty()
        wind_dir_placeholder.empty()
        wind_speed = 0.1
        wind_dir = np.pi / 4
        st.session_state['plot_placeholder'].empty()

    # Parameters
    radius = 15

    Nx = 400 # Number of cells in x direction
    Ny = 100 # Number of cells in y direction
    tau = 0.53 # Relaxation time
    Nt = 20000 # Number of iterations

    shape = create_cylinder(Ny, Nx, radius)
    # Lattice speeds and weights
    NL = 9
    cxs = np.array([0, 0, 1, 1,  1,  0, -1, -1, -1]) 
    cys = np.array([0, 1, 1, 0, -1, -1, -1,  0,  1])
    weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])

    # Source location
    spread = Ny // (num_sources)
    start = Ny // 2 - spread * (num_sources - 1) // 2
    end = Ny // 2 + spread * (num_sources - 1) // 2
    sources_x = np.array([0] * num_sources)
    sources_y = np.linspace(start, end, num_sources).astype(int)

    # Wind
    wind_cx = int(wind_speed * np.cos(wind_dir))
    wind_cy = int(wind_speed * np.sin(wind_dir))

    # Initial conditions
    F = np.ones((Ny, Nx, NL)) + 0.01 * np.random.randn(Ny, Nx, NL)
    F[:, :, 3] = 2.3

    # Boundary conditions
    radius = 13

    if shape_select == "Circle":
        shape = create_cylinder(Ny, Nx, 13)
    elif shape_select == "Bullet":
        shape = create_from_img("bullet.png", Ny, Nx, y=0, x=100, radius=100)
    elif shape_select == "Cow":
        shape = create_from_img("cow.png", Ny, Nx, y=0, x=100, radius=100)
    
    # Create a placeholder for the plot
    st.session_state['plot_placeholder'] = st.empty()

    # Main loop
    for it in range(Nt):

        # Add source
        if source:
            F[sources_y, sources_x, 3] = source_strength

        # Streaming
        for i, cx, cy in zip(range(NL), cxs, cys):
            F[:, :, i] = np.roll(F[:, :, i], cx + wind_cx, axis=1)
            F[:, :, i] = np.roll(F[:, :, i], cy + wind_cy, axis=0)

        # Collision
        rho = np.sum(F, axis=2) # Density
        ux = np.sum(F * cxs, axis=2) / rho # Macroscopic x velocity (velocity of lattice as 1 number)
        uy = np.sum(F * cys, axis=2) / rho # Macroscopic y velocity 

        # Equilibrium distribution
        Feq = create_feq(rho, ux, uy, weights, cxs, cys, NL, F.shape)
            
        # BGK relaxation -> The F distribution tends towards the Feq distribution 
        F += -(1/tau) * (F - Feq)

        # Boundary conditions
        bndryF = F[shape, :]
        bndryF = bndryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]] # Reverse the order of the boundary nodes
        F[shape, :] = bndryF
        ux[shape] = 0 # Ensure the macroscopic velocities at the boundaries are 0
        uy[shape] = 0

        # Plotting
        if (it % plot_every == 0):
            curl = calc_curl(ux, uy)
            plot(curl, shape)

if __name__ == "__main__":
    main()
