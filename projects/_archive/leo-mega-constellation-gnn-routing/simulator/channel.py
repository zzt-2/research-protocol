"""ISL channel model: Shannon capacity + propagation delay."""
import numpy as np
from config import C_LIGHT, ISL_BANDWIDTH, ISL_SNR_REF, ISL_D_REF


def isl_capacity(distances, bw=ISL_BANDWIDTH, snr_ref=ISL_SNR_REF, d_ref=ISL_D_REF):
    """Shannon capacity C = B * log2(1 + SNR(d)).

    SNR follows inverse-square law: SNR(d) = snr_ref * (d_ref / d)^2.
    Returns capacity in bps.
    """
    safe_dist = np.maximum(distances, 1.0)  # avoid division by zero
    snr = snr_ref * (d_ref / safe_dist) ** 2
    return bw * np.log2(1 + snr)


def isl_delay(distances):
    """Propagation delay in seconds."""
    return distances / C_LIGHT


def isl_delay_ms(distances):
    """Propagation delay in milliseconds."""
    return distances / C_LIGHT * 1000
