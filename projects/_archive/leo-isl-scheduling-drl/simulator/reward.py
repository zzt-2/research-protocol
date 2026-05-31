"""M7: RewardCalculator — r = w1·R_tput - w2·C_switch - w3·C_setup.

All terms normalized to [0,1]. Total range [-0.5, 1.0].
"""

import numpy as np
from . import config


class RewardCalculator:
    def __init__(self, w_throughput=None, w_switch=None, w_setup=None):
        self.w1 = w_throughput if w_throughput is not None else config.W_THROUGHPUT
        self.w2 = w_switch if w_switch is not None else config.W_SWITCH
        self.w3 = w_setup if w_setup is not None else config.W_SETUP

    def compute(self, routing_result, n_changed, n_new, setup_delays, n_active_prev):
        """Compute reward and breakdown.

        Args:
            routing_result: dict from Router.route().
            n_changed: number of ISL state changes this step.
            n_new: number of newly established ISLs.
            setup_delays: list of setup delays (seconds) for new ISLs.
            n_active_prev: number of active ISLs in previous step.

        Returns:
            dict with R_tput, C_switch, C_setup, total, and abs breakdown.
        """
        delivered = routing_result.get('delivered', 0)
        demanded = routing_result.get('total_demand', 0)

        # R_tput: normalized throughput
        r_tput = delivered / demanded if demanded > 0 else 0.0

        # C_switch: change ratio (capped at 1.0)
        c_switch = min(n_changed / max(n_active_prev, 1), 1.0)

        # C_setup: normalized setup cost (capped at 1.0)
        total_setup = sum(setup_delays)
        max_possible_setup = n_new * config.SETUP_DELAY_MAX
        c_setup = min(total_setup / max(max_possible_setup, 1.0), 1.0)

        total = self.w1 * r_tput - self.w2 * c_switch - self.w3 * c_setup

        return {
            'R_tput': r_tput,
            'C_switch': c_switch,
            'C_setup': c_setup,
            'w1_R_tput': self.w1 * r_tput,
            'w2_C_switch': self.w2 * c_switch,
            'w3_C_setup': self.w3 * c_setup,
            'total': total,
            'abs_breakdown': {
                'throughput': abs(self.w1 * r_tput),
                'switch': abs(self.w2 * c_switch),
                'setup': abs(self.w3 * c_setup),
            },
        }
