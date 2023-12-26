from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    # load the dataset
    ds = np.load(filename)
    # recenters the dataset to have 'almost' a mean of 0
    ds = ds - np.mean(ds, axis=0)
    
    return ds

def get_covariance(dataset):
    return np.dot(dataset.T, dataset) / (dataset.shape[0] - 1)

def get_eig(S, m):
    eigvals, eigvecs = eigh(S, subset_by_index=[S.shape[0] - m, S.shape[0] - 1])
    # Return the largest m eigenvalues as a diagonal matrix in reversed order
    eigvals = np.diag(eigvals[::-1])
    # reverse the order of the eigenvectors since the eigenvalues are in reversed order
    eigvecs = eigvecs[:, ::-1]

    return eigvals, eigvecs

def get_eig_prop(S, prop):
    # sum of all eigenvalues, calculate the proportion of variance limit
    proportion_of_variance = np.sum(eigh(S, eigvals_only=True)) * prop
    # recalculate eigenvalues and eigenvectors limited by the proportion of variance limit
    eigvals, eigvecs = eigh(S, subset_by_value=[proportion_of_variance, np.inf])
    # Return the largest m eigenvalues as a diagonal matrix in reversed order
    eigvals = np.diag(eigvals[::-1])
    # reverse the order of the eigenvectors since the eigenvalues are in reversed order
    eigvecs = eigvecs[:, ::-1]
    
    return eigvals, eigvecs

def project_image(image, U):
    # calculate the projection of the image onto the eigenvectors
    projection = np.dot(np.transpose(U), image)
    # reconstruct the image from the projection
    reconstruction = np.dot(projection, U.T)

    return reconstruction

def display_image(orig, proj):
    # reshape the original image and the projection, transpose to rotate the image
    orig = np.transpose(orig.reshape(32, 32))
    proj = np.transpose(proj.reshape(32, 32))
    # plot the original image and the projection
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)
    ax1.set_title('Original')
    ax1_pos = ax1.imshow(orig, cmap='viridis', aspect='equal')
    ax2.set_title('Projection')
    ax2_pos = ax2.imshow(proj, cmap='viridis', aspect='equal')
    # add colorbars to the images
    fig.colorbar(ax1_pos)
    fig.colorbar(ax2_pos)

    return fig, ax1, ax2