import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def plot(Z, boundary):
    plt.close()

    # Create a color map for the boundary
    cmap = plt.cm.binary
    cmap.set_bad(color='none')

    # Mask the non-boundary points
    Z_masked = np.ma.array(Z, mask=np.logical_not(boundary))

    # Create a new figure
    fig, ax = plt.subplots()

    # Plot the lattice
    ax.imshow(Z, cmap="bwr", interpolation='none')

    # Overlay the boundary on the lattice
    ax.imshow(Z_masked, cmap=cmap, interpolation='none', alpha=0.7)

    # Display the figure in Streamlit
    st.session_state['plot_placeholder'].pyplot(fig)