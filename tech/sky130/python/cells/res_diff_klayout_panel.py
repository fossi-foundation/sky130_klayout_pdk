# Copyright 2022 Mabrains LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from .res_klayout_panel import res
from .res_diff_child import res_diff_draw

# ################constants################
L_MIN = 2.1
W_MIN = 0.42
# ##############sheet resistances
RES_ND_LVT = 772.2  # sheet res for sky130_fd_pr__res_nd_lvt
RES_ND_HVT = 714.28  # sheet res for sky130_fd_pr__res_nd_hvt
RES_PD = 1172.33  # sheet res for sky130_fd_pr__res_pd_lvt,hvt
##########################################


class res_diff(res):
    """child class for the front end of the diff res (klayout panel)
    Args:
        res(class): parent class for all types of resistors
        l_min(float): minimum length of the resistor
        w_min(float): minimum width of the resistor

    """

    def __init__(self):
        super().__init__(L_MIN, W_MIN)  # (l_min,w_min)

        # types of resistor you need to add
        # it goes in var self.type

        self.Type_handle.add_choice(
            "sky130_fd_pr__res_nd_lvt", "sky130_fd_pr__res_nd_lvt"
        )
        self.Type_handle.add_choice(
            "sky130_fd_pr__res_nd_hvt", "sky130_fd_pr__res_nd_hvt"
        )

        self.Type_handle.add_choice(
            "sky130_fd_pr__res_pd_lvt", "sky130_fd_pr__res_pd_lvt"
        )
        self.Type_handle.add_choice(
            "sky130_fd_pr__res_pd_hvt", "sky130_fd_pr__res_pd_hvt"
        )

        self.Type_handle.default = self.Type_handle.choice_values()[0]

    def coerce_parameters_impl(self):
        """(override func) check the minimum values of l and w

        decide whether the handle or the numeric parameter has
        changed (by comparing against the effective
        radius ru) and set ru to the effective radius. We also update the
        numerical value or the shape, depending on which on has not changed


        """
        super().coerce_parameters_impl(L_MIN, W_MIN)  # (l_min,w_min)
        # res_value = sheet res * area
        if self.type == "sky130_fd_pr__res_nd_lvt":
            self.res_value = RES_ND_LVT * self.area
        elif self.type == "sky130_fd_pr__res_nd_hvt":
            self.res_value = RES_ND_HVT * self.area
        else:
            self.res_value = RES_PD * self.area

    def produce_impl(self):
        """(override func)call the implementation backend code
        """
        drw = res_diff_draw(self.type)
        drw.your_res(
            self.cell, l=self.len, w=self.w, type=self.type, gr=self.gr
        )
