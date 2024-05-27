import numpy as np


class Scattering_geometry:
    def __init__(self, energy, lattice_parameter, ref_in, ref_out):
        """
        Initialize the Scattering_geometry with energy, lattice parameters, and reference vectors.

        Parameters:
        energy (float): Energy value.
        lattice_parameter (list): Lattice parameters [a, b, c, alpha, beta, gamma].
        ref_in (list): Reference vector for the in-plane direction [h, k, l].
        ref_out (list): Reference vector for the out-of-plane direction [h, k, l].
        """
        self.energy = energy
        self.lattice_parameter = lattice_parameter
        self.ref_in = ref_in
        self.ref_out = ref_out
        self.k_in, self.k_out = self._calculate_projector()

    def _calculate_projector(self):
        """
        Calculate normalization factors for the in-plane and out-of-plane components
        based on the given energy, lattice parameters, and reference vectors.

        Returns:
        tuple: Normalization factors (k_in, k_out).
        """
        a, b, c, alpha, beta, gamma = self.lattice_parameter

        # Calculate reciprocal lattice vectors
        b1, b2, b3 = self._lattice_parameters_to_vectors(self.lattice_parameter)

        # Calculate magnitudes of reciprocal lattice vectors for normalization
        k_in = np.linalg.norm(np.dot(self.ref_in, [b1, b2, b3]))
        k_out = np.linalg.norm(np.dot(self.ref_out, [b1, b2, b3]))

        return k_in, k_out

    def _lattice_parameters_to_vectors(self, parameters):
        """
        Convert lattice parameters to reciprocal lattice vectors.

        Parameters:
        parameters (list): Lattice parameters [a, b, c, alpha, beta, gamma]

        Returns:
        tuple: Reciprocal lattice vectors (b1, b2, b3)
        """
        a, b, c, alpha, beta, gamma = parameters

        # Convert angles to radians
        alpha_rad = np.radians(alpha)
        beta_rad = np.radians(beta)
        gamma_rad = np.radians(gamma)

        # Calculate unit cell vectors
        a1 = np.array([a, 0, 0])
        a2 = np.array([b * np.cos(gamma_rad), b * np.sin(gamma_rad), 0])
        a3_x = c * np.cos(beta_rad)
        a3_y = (b * c * np.cos(alpha_rad) - a2[0] * a3_x) / a2[1]
        a3 = np.array([a3_x, a3_y, np.sqrt(c**2 - a3_x**2 - a3_y**2)])

        # Calculate reciprocal lattice vectors
        V = np.dot(a1, np.cross(a2, a3))
        b1 = 2 * np.pi * np.cross(a2, a3) / V
        b2 = 2 * np.pi * np.cross(a3, a1) / V
        b3 = 2 * np.pi * np.cross(a1, a2) / V

        return b1, b2, b3

    def geo_to_q(self, alpha, beta):
        """
        Convert geometric angles alpha and beta back to wave vector components q_in and q_out.

        Parameters:
        alpha (float): Incident angle in degrees.
        beta (float): Exist angle in degrees.

        Returns:
        tuple: Wave vector components (q_in, q_out).
        """
        # Calculate the two_theta and delta angle in degrees
        two_theta = alpha + beta
        delta = (alpha - beta) / 2

        # Calculate the magnitude of the wave vector
        q_magnitude = 2 * np.sin(np.radians(two_theta / 2)) * (self.energy / 1973)

        # Calculate the in-plane component of the wave vector
        q_in = q_magnitude * np.sin(np.radians(delta)) / self.k_in

        # Calculate the out-of-plane component of the wave vector
        q_out = q_magnitude * np.cos(np.radians(delta)) / self.k_out

        return q_in, q_out

    def q_to_geo(self, q_in, q_out):
        """
        Convert wave vector components to geometric angles alpha and beta.

        Parameters:
        q_in (float): In-plane component of the wave vector.
        q_out (float): Out-of-plane component of the wave vector.

        Returns:
        tuple: Angles (alpha, beta) in degrees.
        """
        # Calculate the magnitude of the wave vector
        q_magnitude = np.sqrt((q_in * self.k_in) ** 2 + (q_out * self.k_out) ** 2)

        # Calculate the two_theta angle in radians
        two_theta = 2 * np.arcsin(q_magnitude / 2 / (self.energy / 1973))

        # Calculate the delta angle in radians
        delta = np.arctan(q_in * self.k_in / (q_out * self.k_out))

        # Calculate the alpha angle in degrees
        alpha = (np.degrees(two_theta + delta * 2)) / 2

        # Calculate the beta angle in degrees
        beta = (np.degrees(two_theta - delta * 2)) / 2

        return alpha, beta


# Example usage
if __name__ == "__main__":
    energy = 708
    lattice_parameter = [3.99, 3.99, 16.299, 90, 90, 120]
    ref_in = [1, 0, 0]
    ref_out = [0, 0, 1]

    # Initialize the Scattering_geometry class
    converter = Scattering_geometry(energy, lattice_parameter, ref_in, ref_out)

    # Example angles
    alpha, beta = 10, 40

    # Convert angles to wave vector components
    q_in, q_out = converter.geo_to_q(alpha, beta)
    print(f"q_in: {q_in}, q_out: {q_out}")

    # Convert wave vector components back to angles
    alpha, beta = converter.q_to_geo(q_in, q_out)
    print(f"alpha: {alpha}, beta: {beta}")
