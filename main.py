import io
import os
import pathlib
from io import StringIO, BytesIO
from pathlib import Path
from typing import Literal, List

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from utils import parse_xvg, legend_locations

st.set_page_config(layout="wide", page_title="XVG Plotter")

if "single_img" not in st.session_state:
    st.session_state.single_img = BytesIO()
if "single_file_name" not in st.session_state:
    st.session_state.single_file_name = None
if "single_title" not in st.session_state:
    st.session_state.single_title = None
if "single_title_updated" not in st.session_state:
    st.session_state.single_title_updated = ""
if "single_title_size" not in st.session_state:
    st.session_state.single_title_size = 20
if "single_title_show" not in st.session_state:
    st.session_state.single_title_show = False
if "single_title_loc" not in st.session_state:
    st.session_state.single_title_loc: Literal["left", "center", "right"] | None = "center"
if "single_xaxis" not in st.session_state:
    st.session_state.single_xaxis = None
if "single_xaxis_updated" not in st.session_state:
    st.session_state.single_xaxis_updated = None
if "single_yaxis" not in st.session_state:
    st.session_state.single_yaxis = None
if "single_yaxis_updated" not in st.session_state:
    st.session_state.single_yaxis_updated = None
if "single_yaxes" not in st.session_state:
    st.session_state.single_yaxes = []
if "single_x_index" not in st.session_state:
    st.session_state.single_x_index = 0
if "single_y_index" not in st.session_state:
    st.session_state.single_y_index = 1
if "single_xvg_file_name" not in st.session_state:
    st.session_state.single_xvg_file_name = None
if "single_label_size" not in st.session_state:
    st.session_state.single_label_size = 16
if "single_legend_show" not in st.session_state:
    st.session_state.single_legend_show = False
if "single_legend_loc" not in st.session_state:
    st.session_state.single_legend_loc = "best"
if "single_legend_size" not in st.session_state:
    st.session_state.single_legend_size = 12
if "single_series" not in st.session_state:
    st.session_state.single_series = []
if "single_plot_show" not in st.session_state:
    st.session_state.single_plot_show = False
if "single_multiply_x" not in st.session_state:
    st.session_state.single_multiply_x = False
if "single_x_multiplication_value" not in st.session_state:
    st.session_state.single_x_multiplication_value = 1
if "single_multiply_y" not in st.session_state:
    st.session_state.single_multiply_y = False
if "single_y_multiplication_value" not in st.session_state:
    st.session_state.single_y_multiplication_value = 1
if "single_modify_data" not in st.session_state:
    st.session_state.single_modify_data = False
if "single_modify_min" not in st.session_state:
    st.session_state.single_modify_min = 1
if "single_modify_max" not in st.session_state:
    st.session_state.single_modify_max = 1
if "single_modify_step" not in st.session_state:
    st.session_state.single_modify_step = 1
if "single_x_lim" not in st.session_state:
    st.session_state.single_x_lim = False
if "single_x_lim_min" not in st.session_state:
    st.session_state.single_x_lim_min = 1
if "single_x_lim_max" not in st.session_state:
    st.session_state.single_x_lim_max = 1
if "single_y_lim" not in st.session_state:
    st.session_state.single_y_lim = False
if "single_y_lim_min" not in st.session_state:
    st.session_state.single_y_lim_min = 1
if "single_y_lim_max" not in st.session_state:
    st.session_state.single_y_lim_max = 1
if "single_csv_data" not in st.session_state:
    st.session_state.single_csv_data = []
if "single_line_opacity_show" not in st.session_state:
    st.session_state.single_line_opacity_show = False
if "single_line_opacity" not in st.session_state:
    st.session_state.single_line_opacity = 1.00
if "single_line2_opacity" not in st.session_state:
    st.session_state.single_line2_opacity = 1.00

if "multiple_img" not in st.session_state:
    st.session_state.multiple_img = BytesIO()
if "multiple_file_name" not in st.session_state:
    st.session_state.multiple_file_name = None
if "multiple_project_folder" not in st.session_state:
    st.session_state.multiple_project_folder = ""
if "multiple_plotter_folder" not in st.session_state:
    st.session_state.multiple_plotter_folder = ""
if "multiple_xvg_files" not in st.session_state:
    st.session_state.multiple_xvg_files = []
if "multiple_xvg_file_name" not in st.session_state:
    st.session_state.multiple_xvg_file_name = None
if "multiple_title" not in st.session_state:
    st.session_state.multiple_title = None
if "multiple_title_updated" not in st.session_state:
    st.session_state.multiple_title_updated = ""
if "multiple_title_size" not in st.session_state:
    st.session_state.multiple_title_size = 20
if "multiple_title_show" not in st.session_state:
    st.session_state.multiple_title_show = False
if "multiple_title_loc" not in st.session_state:
    st.session_state.multiple_title_loc: Literal["left", "center", "right"] | None = "center"
if "multiple_series" not in st.session_state:
    st.session_state.multiple_series = []
if "multiple_xaxis" not in st.session_state:
    st.session_state.multiple_xaxis = None
if "multiple_xaxis_updated" not in st.session_state:
    st.session_state.multiple_xaxis_updated = None
if "multiple_yaxis" not in st.session_state:
    st.session_state.multiple_yaxis = None
if "multiple_yaxis_updated" not in st.session_state:
    st.session_state.multiple_yaxis_updated = None
if "multiple_yaxes" not in st.session_state:
    st.session_state.multiple_yaxes = []
if "multiple_x_index" not in st.session_state:
    st.session_state.multiple_x_index = 0
if "multiple_y_index" not in st.session_state:
    st.session_state.multiple_y_index = 1
if "multiple_label_size" not in st.session_state:
    st.session_state.multiple_label_size = 16
if "multiple_legend_show" not in st.session_state:
    st.session_state.multiple_legend_show = False
if "multiple_legend_loc" not in st.session_state:
    st.session_state.multiple_legend_loc = "best"
if "multiple_legend_size" not in st.session_state:
    st.session_state.multiple_legend_size = 12
if "multiple_multiply_x" not in st.session_state:
    st.session_state.multiple_multiply_x = False
if "multiple_x_multiplication_value" not in st.session_state:
    st.session_state.multiple_x_multiplication_value = 1
if "multiple_multiply_y" not in st.session_state:
    st.session_state.multiple_multiply_y = False
if "multiple_y_multiplication_value" not in st.session_state:
    st.session_state.multiple_y_multiplication_value = 1
if "multiple_modify_data" not in st.session_state:
    st.session_state.multiple_modify_data = False
if "multiple_modify_min" not in st.session_state:
    st.session_state.multiple_modify_min = 1
if "multiple_modify_max" not in st.session_state:
    st.session_state.multiple_modify_max = 1
if "multiple_modify_step" not in st.session_state:
    st.session_state.multiple_modify_step = 1
if "multiple_x_lim" not in st.session_state:
    st.session_state.multiple_x_lim = False
if "multiple_x_lim_min" not in st.session_state:
    st.session_state.multiple_x_lim_min = 1
if "multiple_x_lim_max" not in st.session_state:
    st.session_state.multiple_x_lim_max = 1
if "multiple_y_lim" not in st.session_state:
    st.session_state.multiple_y_lim = False
if "multiple_y_lim_min" not in st.session_state:
    st.session_state.multiple_y_lim_min = 1
if "multiple_y_lim_max" not in st.session_state:
    st.session_state.multiple_y_lim_max = 1
if "multiple_csv_data" not in st.session_state:
    st.session_state.multiple_csv_data = []
if "multiple_line_opacity_show" not in st.session_state:
    st.session_state.multiple_line_opacity_show = False
if "multiple_line_opacity" not in st.session_state:
    st.session_state.multiple_line_opacity = 1.00

if "docker_project_path" not in st.session_state:
    st.session_state.docker_project_path: pathlib.Path = Path("/projects")
if "docker_directories" not in st.session_state:
    st.session_state.docker_directories: List[pathlib.Path] = []
if "docker_selected_dir" not in st.session_state:
    st.session_state.docker_selected_dir = None
if "docker_xvg_files" not in st.session_state:
    st.session_state.docker_xvg_files: List[pathlib.Path] = []

hide_st_style = """
<style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

selected = option_menu(
    None, ["Single File Analysis", "Comparison Analysis", "Folder Analysis", "Documentation"],
    icons=['cloud-upload', "arrows-collapse-vertical", "list-task", "file-earmark-medical"],
    menu_icon="cast", default_index=0, orientation="horizontal"
)


def main_options(value: str, xvg, string_data: str):
    metadata, data = parse_xvg(string_data)

    st.session_state[f"{value}_title"] = metadata["title"]
    st.session_state[f"{value}_series"] = metadata["labels"]["series"]
    st.session_state[f"{value}_xaxis"] = metadata["labels"]["xaxis"]
    st.session_state[f"{value}_yaxis"] = metadata["labels"]["yaxis"]

    xvg_file_value: str = ""
    if value == "single":
        st.session_state[f"{value}_xvg_file_name"] = os.path.splitext(xvg.name)[0]
        xvg_file_value = st.session_state[f"{value}_xvg_file_name"]
    elif value == "multiple":
        xvg_file_value = os.path.splitext(st.session_state[f"{value}_xvg_file_name"])[0]

    file_name_columns = st.columns([1])
    file_name_columns[0].text_input(label="File Name", value=xvg_file_value,
                                    key=f"{value}_file_name")

    axis_columns = st.columns([1, 2])
    x_index_ = axis_columns[0].radio("Select X Axis",
                                     [st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"],
                                     index=0)
    y_index__ = axis_columns[1].multiselect(
        'Select Y Axes',
        [st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"],
        default=([st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"])[
            1 if len(st.session_state[f"{value}_series"]) else 0]
    )

    st.session_state[f"{value}_x_index"] = (
            [st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"]).index(
        x_index_)
    st.session_state[f"{value}_yaxes"] = list(
        map(lambda z: ([st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"]).index(z),
            y_index__))

    return data


def main_options_comparison(value: str, xvg, string_data1: str, string_data2: str):
    metadata, data = parse_xvg(string_data1)
    metadata2, data2 = parse_xvg(string_data2)

    st.session_state[f"{value}_title"] = metadata["title"]
    st.session_state[f"{value}_series"] = metadata["labels"]["series"]
    st.session_state[f"{value}_xaxis"] = metadata["labels"]["xaxis"]
    st.session_state[f"{value}_yaxis"] = metadata["labels"]["yaxis"]

    xvg_file_value: str = ""
    if value == "single":
        st.session_state[f"{value}_xvg_file_name"] = os.path.splitext(xvg.name)[0]
        xvg_file_value = st.session_state[f"{value}_xvg_file_name"]
    elif value == "multiple":
        xvg_file_value = os.path.splitext(st.session_state[f"{value}_xvg_file_name"])[0]

    file_name_columns = st.columns([1])
    file_name_columns[0].text_input(label="File Name", value=xvg_file_value,
                                    key=f"{value}_file_name")

    axis_columns = st.columns([1, 2])
    x_index_ = axis_columns[0].radio("Select X Axis",
                                     [st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"],
                                     index=0)
    y_index__ = axis_columns[1].multiselect(
        'Select Y Axes',
        [st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"],
        default=([st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"])[
            1 if len(st.session_state[f"{value}_series"]) else 0]
    )

    st.session_state[f"{value}_x_index"] = (
            [st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"]).index(
        x_index_)
    st.session_state[f"{value}_yaxes"] = list(
        map(lambda z: ([st.session_state[f"{value}_xaxis"]] + st.session_state[f"{value}_series"]).index(z),
            y_index__))

    return data, data2


def label_options(value: str):
    label_columns = st.columns([1, 1])
    label_columns[0].text_input(label="X Label", value=st.session_state[f"{value}_xaxis"],
                                key=f"{value}_xaxis_updated")
    label_columns[1].text_input(label="Y Label", value=st.session_state[f"{value}_yaxis"],
                                key=f"{value}_yaxis_updated")

    size_columns = st.columns([1])
    size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16,
                           key=f"{value}_label_size")

    return label_columns, size_columns


def title_options(value: str):
    columns = st.columns([1, 1, 1])
    columns[0].checkbox(label="Show Title?", key=f"{value}_title_show")
    columns[0].text_input(label="Title", value=st.session_state[f"{value}_title"],
                          key=f"{value}_title_updated")
    columns[1].slider(label="Title Size", min_value=12, max_value=30, step=1, value=20,
                      key=f"{value}_title_size")
    columns[2].selectbox(label="Title Location", key=f"{value}_title_loc",
                         options=["center", "left", "right"], index=0)

    return columns


def legend_options(value: str):
    columns = st.columns([1, 1, 1])
    columns[0].checkbox(label="Show Legend?", key=f"{value}_legend_show")
    columns[1].slider(label="Legend Size", min_value=8, max_value=24, step=1, value=12,
                      key=f"{value}_legend_size")
    columns[2].selectbox(label="Legend Location", key=f"{value}_legend_loc",
                         options=legend_locations,
                         index=0)

    return columns


def axis_multiplication_options(value: str):
    multiplier_x_column = st.columns([1, 3, 1])
    multiplier_x_column[0].checkbox(label="Multiply X Axis?", key=f"{value}_multiply_x")
    multiplier_x_column[1].number_input(label="Multiplication Value", value=1.0000,
                                        key=f"{value}_x_multiplication_value")
    with multiplier_x_column[2]:
        st.text_input("Value", value=st.session_state[f"{value}_x_multiplication_value"], disabled=True,
                      key=f"{value}_x_show_value")

    multiplier_y_column = st.columns([1, 3, 1])
    multiplier_y_column[0].checkbox(label="Multiply Y Axis?", key=f"{value}_multiply_y")
    multiplier_y_column[1].number_input(label="Multiplication Value", value=1.0000,
                                        key=f"{value}_y_multiplication_value")
    with multiplier_y_column[2]:
        st.text_input("Value", value=st.session_state[f"{value}_y_multiplication_value"], disabled=True,
                      key=f"{value}_y_show_value")

    return multiplier_x_column, multiplier_y_column


def modifier_options(value: str, points: int):
    modifier_selector_columns = st.columns([1, 1, 1])
    modifier_selector_columns[0].checkbox(label="Modify data?", key=f"{value}_modify_data")
    modifier_selector_columns[1].write(f"Total data points: {points}")

    modifier_columns = st.columns([1, 1, 1])
    modifier_columns[0].number_input(
        label="Start Point", value=0,
        key=f"{value}_modify_min",
    )
    modifier_columns[1].number_input(
        label="End Point", value=points,
        key=f"{value}_modify_max"
    )
    modifier_columns[2].number_input(
        label="Step", value=1,
        key=f"{value}_modify_step"
    )

    return modifier_selector_columns, modifier_columns


def limit_options(value: str):
    x_columns = st.columns([1, 1, 1])
    x_columns[0].checkbox(label="Limit X Axis?", key=f"{value}_x_lim")
    x_columns[1].number_input(
        label="Min", value=1.000,
        key=f"{value}_x_lim_min"
    )
    x_columns[2].number_input(
        label="Max", value=1.000,
        key=f"{value}_x_lim_max"
    )

    y_columns = st.columns([1, 1, 1])
    y_columns[0].checkbox(label="Limit Y Axis?", key=f"{value}_y_lim")
    y_columns[1].number_input(
        label="Min", value=1.000,
        key=f"{value}_y_lim_min"
    )
    y_columns[2].number_input(
        label="Max", value=1.000,
        key=f"{value}_y_lim_max"
    )

    return x_columns, y_columns


def opacity_options(value: str):
    if selected == "Comparison Analysis":
        columns = st.columns([1, 1, 1])
        columns[0].checkbox(label="Reduce Opacity?", key=f"{value}_line_opacity_show")
        columns[1].slider(label="Line 1 Opacity", min_value=0.00, max_value=1.00, step=0.01,
                          value=st.session_state[f"{value}_line_opacity"],
                          key=f"{value}_line_opacity")
        columns[2].slider(label="Line 2 Opacity", min_value=0.00, max_value=1.00, step=0.01,
                          value=st.session_state[f"{value}_line2_opacity"],
                          key=f"{value}_line2_opacity")

    else:
        columns = st.columns([1, 1])
        columns[0].checkbox(label="Reduce Opacity?", key=f"{value}_line_opacity_show")
        columns[1].slider(label="Line Opacity", min_value=0.00, max_value=1.00, step=0.01,
                          value=st.session_state[f"{value}_line_opacity"],
                          key=f"{value}_line_opacity")

    return columns


def plotting(value: str, data: npt.NDArray, columns):
    if st.session_state[f"{value}_file_name"] and st.session_state[f"{value}_xaxis"] and st.session_state[
        f"{value}_yaxis"] and st.session_state[f"{value}_label_size"]:
        data_shape = 0

        for y in st.session_state[f"{value}_yaxes"]:
            if st.session_state[f"{value}_multiply_y"]:
                y_multiplier = st.session_state[f"{value}_y_multiplication_value"]
            else:
                y_multiplier = 1

            if st.session_state[f"{value}_multiply_x"]:
                x_multiplier = st.session_state[f"{value}_x_multiplication_value"]
            else:
                x_multiplier = 1

            new_data = data
            if st.session_state[f"{value}_modify_data"]:
                new_data = new_data[
                           st.session_state[f"{value}_modify_min"]:st.session_state[f"{value}_modify_max"]:
                           st.session_state[
                               f"{value}_modify_step"]]

            st.session_state[f"{value}_csv_data"] = new_data

            data_shape = new_data.shape[0]

            plt.plot(new_data[..., st.session_state[f"{value}_x_index"]] * x_multiplier,
                     new_data[..., y] * y_multiplier,
                     alpha=st.session_state[f"{value}_line_opacity"] if st.session_state[
                         f"{value}_line_opacity_show"] else 1)

        columns[2].write(f"Current data points: {data_shape}")

        if st.session_state[f"{value}_legend_show"]:
            plt.legend(st.session_state[f"{value}_series"], loc=st.session_state[f"{value}_legend_loc"],
                       fontsize=st.session_state[f"{value}_legend_size"])
        if st.session_state[f"{value}_title_show"]:
            plt.title(label=st.session_state[f"{value}_title_updated"],
                      loc=st.session_state[f"{value}_title_loc"],
                      fontdict={"fontsize": st.session_state[f"{value}_title_size"]}, pad=16)
        xaxis_updated = st.session_state[f'{value}_xaxis_updated']
        yaxis_updated = st.session_state[f'{value}_yaxis_updated']
        plt.xlabel(fr"{xaxis_updated}",
                   fontsize=st.session_state[f"{value}_label_size"])
        plt.ylabel(fr"{yaxis_updated}",
                   fontsize=st.session_state[f"{value}_label_size"])
        if st.session_state[f'{value}_x_lim']:
            plt.xlim(st.session_state[f'{value}_x_lim_min'], st.session_state[f'{value}_x_lim_max'])
        if st.session_state[f'{value}_y_lim']:
            plt.ylim(st.session_state[f'{value}_y_lim_min'], st.session_state[f'{value}_y_lim_max'])

        plt.savefig(st.session_state[f"{value}_img"], format='png', dpi=600)

        st.session_state[f"{value}_plot_show"] = True


def plotting_comparison(value: str, data: npt.NDArray, data1: npt.NDArray, columns):
    if st.session_state[f"{value}_file_name"] and st.session_state[f"{value}_xaxis"] and st.session_state[
        f"{value}_yaxis"] and st.session_state[f"{value}_label_size"]:
        data_shape = 0

        for y in st.session_state[f"{value}_yaxes"]:
            if st.session_state[f"{value}_multiply_y"]:
                y_multiplier = st.session_state[f"{value}_y_multiplication_value"]
            else:
                y_multiplier = 1

            if st.session_state[f"{value}_multiply_x"]:
                x_multiplier = st.session_state[f"{value}_x_multiplication_value"]
            else:
                x_multiplier = 1

            new_data = data
            new_data1 = data1
            if st.session_state[f"{value}_modify_data"]:
                new_data = new_data[
                           st.session_state[f"{value}_modify_min"]:st.session_state[f"{value}_modify_max"]:
                           st.session_state[
                               f"{value}_modify_step"]]
                new_data1 = new_data1[
                            st.session_state[f"{value}_modify_min"]:st.session_state[f"{value}_modify_max"]:
                            st.session_state[
                                f"{value}_modify_step"]]

            data_shape = new_data.shape[0]

            plt.plot(new_data[..., st.session_state[f"{value}_x_index"]] * x_multiplier,
                     new_data[..., y] * y_multiplier,
                     alpha=st.session_state[f"{value}_line_opacity"] if st.session_state[
                         f"{value}_line_opacity_show"] else 1)
            plt.plot(new_data1[..., st.session_state[f"{value}_x_index"]] * x_multiplier,
                     new_data1[..., y] * y_multiplier,
                     alpha=st.session_state[f"{value}_line2_opacity"] if st.session_state[
                         f"{value}_line_opacity_show"] else 1)

            st.session_state[f"{value}_csv_data"] = np.hstack((new_data, new_data1))

        columns[2].write(f"Current data points: {data_shape}")

        if st.session_state[f"{value}_legend_show"]:
            plt.legend(st.session_state[f"{value}_series"], loc=st.session_state[f"{value}_legend_loc"],
                       fontsize=st.session_state[f"{value}_legend_size"])
        if st.session_state[f"{value}_title_show"]:
            plt.title(label=st.session_state[f"{value}_title_updated"],
                      loc=st.session_state[f"{value}_title_loc"],
                      fontdict={"fontsize": st.session_state[f"{value}_title_size"]}, pad=16)
        xaxis_updated = st.session_state[f'{value}_xaxis_updated']
        yaxis_updated = st.session_state[f'{value}_yaxis_updated']
        plt.xlabel(fr"{xaxis_updated}",
                   fontsize=st.session_state[f"{value}_label_size"])
        plt.ylabel(fr"{yaxis_updated}",
                   fontsize=st.session_state[f"{value}_label_size"])
        plt.savefig(st.session_state[f"{value}_img"], format='png', dpi=600)

        st.session_state[f"{value}_plot_show"] = True


def plotter(value: str):
    with st.container(border=True):
        plot_columns = st.columns([1, 1, 1])
        plot_columns[0].subheader("Visualization")

        file_name = st.session_state[f"{value}_file_name"]

        if st.session_state[f"{value}_img"] and st.session_state[f"{value}_file_name"] and st.session_state[
            f"{value}_plot_show"]:
            with io.BytesIO() as buffer:
                np.savetxt(buffer, st.session_state[f"{value}_csv_data"], delimiter=",")
                plot_columns[1].download_button(
                    label="Download CSV",
                    data=buffer,
                    file_name=f"{file_name}.csv",
                    mime='text/csv'
                )

            plot_columns[2].download_button(
                label="Download Plot",
                data=st.session_state[f"{value}_img"],
                file_name=f"{file_name}.png",
                mime="image/png"
            )

            st.pyplot(plt)

            if selected != "Comparison Analysis":
                if st.button("Show Data Points"):
                    raw_range = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]

                    converted_range = raw_range[:len(st.session_state[f"{value}_series"])]

                    columns = ["x"] + converted_range

                    df = pd.DataFrame(st.session_state[f"{value}_csv_data"], columns=columns)

                    st.line_chart(df, x="x", y=[converted_range[x - 1] for x in st.session_state[f"{value}_yaxes"]])


if selected == "Single File Analysis":
    wrapper_columns = st.columns([3, 2])

    with wrapper_columns[0]:
        with st.container(border=True):
            files = st.columns([1])
            xvg = files[0].file_uploader(label="Upload XVG File", accept_multiple_files=False, type=["xvg"])

            if xvg is not None:
                with st.expander("Main Options", expanded=True):
                    stringio = StringIO(xvg.getvalue().decode("utf-8"))

                    string_data = stringio.read()

                    data = main_options("single", xvg, string_data)

                with st.expander("Labels"):
                    label_options("single")

                with st.expander("Title"):
                    title_options("single")

                with st.expander("Legends"):
                    legend_options("single")

                with st.expander("Axis Multiplication"):
                    axis_multiplication_options("single")

                with st.expander("Data Modifier"):
                    modifier_selector_columns, modifier_columns = modifier_options("single", data.shape[0])

                with st.expander("Axis Limitation"):
                    limit_options("single")

                with st.expander("Opacity"):
                    opacity_options("single")

                if st.button("Plot XVG"):
                    plotting("single", data, modifier_selector_columns)

    with wrapper_columns[1]:
        plotter("single")

if selected == "Comparison Analysis":
    wrapper_columns = st.columns([3, 2])

    with wrapper_columns[0]:
        with st.container(border=True):
            files = st.columns([1, 1])
            xvg1 = files[0].file_uploader(label="Upload XVG File 1", accept_multiple_files=False, type=["xvg"])
            xvg2 = files[1].file_uploader(label="Upload XVG File 2", accept_multiple_files=False, type=["xvg"])

        if xvg1 is not None and xvg2 is not None:
            with st.expander("Main Options", expanded=True):
                stringio1 = StringIO(xvg1.getvalue().decode("utf-8"))
                stringio2 = StringIO(xvg2.getvalue().decode("utf-8"))

                string_data1 = stringio1.read()
                string_data2 = stringio2.read()

                data1, data2 = main_options_comparison("single", xvg1, string_data1, string_data2)

            with st.expander("Labels"):
                label_options("single")

            with st.expander("Title"):
                title_options("single")

            with st.expander("Legends"):
                legend_options("single")

            with st.expander("Axis Multiplication"):
                axis_multiplication_options("single")

            with st.expander("Data Modifier"):
                modifier_selector_columns, modifier_columns = modifier_options("single", data1.shape[0])

            with st.expander("Axis Limitation"):
                limit_options("single")

            with st.expander("Opacity"):
                opacity_options("single")

            if st.button("Plot XVG"):
                plotting_comparison("single", data1, data2, modifier_selector_columns)

    with wrapper_columns[1]:
        plotter("single")

elif selected == "Folder Analysis":
    IS_DOCKER = int(os.environ.get('IS_DOCKER', "0"))

    if IS_DOCKER:
        wrapper_columns = st.columns([3, 2])

        if st.session_state.docker_project_path:
            st.session_state.docker_directories = []
            for i in st.session_state.docker_project_path.glob('[!.]*'):
                if i.is_dir():
                    st.session_state.docker_directories.append(i.name)


        def handle_next():
            if st.session_state.docker_selected_dir:
                st.session_state.docker_project_path = st.session_state.docker_project_path / st.session_state.docker_selected_dir

                st.session_state.docker_directories = []
                for i in st.session_state.docker_project_path.glob('[!.]*'):
                    if i.is_dir():
                        st.session_state.docker_directories.append(i.name)


        def handle_clear():
            st.session_state.docker_project_path = Path("/projects")
            st.session_state.docker_xvg_files = []

            st.session_state.docker_directories = []
            for i in st.session_state.docker_project_path.glob('[!.]*'):
                if i.is_dir():
                    st.session_state.docker_directories.append(i.name)


        def handle_select():
            if st.session_state.docker_selected_dir:
                st.session_state.docker_project_path = st.session_state.docker_project_path / st.session_state.docker_selected_dir
                st.session_state.docker_xvg_files = [x for x in st.session_state.docker_project_path.iterdir() if
                                                     x.is_file() and x.name.endswith(".xvg")]


        # st.write(st.session_state.docker_xvg_files)

        with wrapper_columns[0]:
            with st.container(border=True):
                folder_columns = st.columns([3, 2])

                with folder_columns[0]:
                    st.selectbox("Select Folder", options=st.session_state.docker_directories, index=None,
                                 key="docker_selected_dir")

                with folder_columns[1]:
                    if st.session_state.docker_project_path:
                        st.write("Selected Folder", st.session_state.docker_project_path)

                # button_wrapper_columns = st.columns([3, 2])
                # with button_wrapper_columns[0]:
                button_columns = st.columns([1, 1, 1, 2])
                button_columns[0].button("Select", on_click=handle_select)
                button_columns[1].button("Next", on_click=handle_next)
                button_columns[2].button("Clear", on_click=handle_clear)

        xvg_columns = st.columns([3, 2])

        with xvg_columns[0]:
            if len(st.session_state.docker_xvg_files):
                st.selectbox("Select XVG File", options=[x.name for x in st.session_state.docker_xvg_files],
                             key="multiple_xvg_file_name", index=None)

                if st.session_state.multiple_xvg_file_name:
                    with st.expander("Main Options", expanded=True):
                        xvg = st.session_state.docker_project_path / st.session_state.multiple_xvg_file_name

                        if xvg is not None:
                            with open(xvg, "rb") as f:
                                string_data = f.read().decode("utf-8")

                            data = main_options("multiple", xvg, string_data)

                    with st.expander("Labels"):
                        label_options("multiple")

                    with st.expander("Title"):
                        title_options("multiple")

                    with st.expander("Legends"):
                        legend_options("multiple")

                    with st.expander("Axis Multiplication"):
                        axis_multiplication_options("multiple")

                    with st.expander("Data Modifier"):
                        modifier_selector_columns, modifier_columns = modifier_options("multiple", data.shape[0])

                    with st.expander("Axis Limitation"):
                        limit_options("multiple")

                    with st.expander("Opacity"):
                        opacity_options("multiple")

                    if st.button("Plot XVG"):
                        plotting("multiple", data, modifier_selector_columns)

        with xvg_columns[1]:
            plotter("multiple")

    else:
        wrapper_columns = st.columns([3, 2])

        with wrapper_columns[0]:
            with st.container(border=True):
                folder_columns = st.columns([3, 2])

                with folder_columns[0]:
                    st.text_input("Put Project Folder", key="multiple_project_folder")

                    if st.button("Submit"):
                        st.session_state.multiple_xvg_files = []

                        with folder_columns[1]:
                            if st.session_state.multiple_project_folder:
                                st.write(f"Targeted folder: {st.session_state.multiple_project_folder}")

                                is_exist = os.path.exists(st.session_state.multiple_project_folder)
                                if is_exist:
                                    files = [f for f in
                                             os.listdir(st.session_state.multiple_project_folder) if
                                             f.endswith(".xvg") and os.path.isfile(
                                                 os.path.join(st.session_state.multiple_project_folder,
                                                              f))]

                                    if len(files):
                                        st.session_state.multiple_xvg_files = files

                                        plotter_folder = os.path.join(st.session_state.multiple_project_folder,
                                                                      "xvg-plotter")
                                        st.session_state.multiple_plotter_folder = plotter_folder

                                        if not os.path.isdir(plotter_folder):
                                            os.makedirs(plotter_folder)

                                        st.success("Project folder selected.")
                                    else:
                                        st.error(
                                            "No XVG files found or files are not showing because of permission issue. Use Single File Analysis instead.")
                                else:
                                    st.error(
                                        "This is not a valid folder or files are not showing because of permission issue. Use Single File Analysis instead.")

                if len(st.session_state.multiple_xvg_files):
                    st.selectbox("Select XVG File", options=st.session_state.multiple_xvg_files,
                                 key="multiple_xvg_file_name")

                    if st.session_state.multiple_xvg_file_name:
                        with st.expander("Main Options", expanded=True):
                            xvg = os.path.join(st.session_state.multiple_project_folder,
                                               st.session_state.multiple_xvg_file_name)

                            if xvg is not None:
                                with open(xvg, 'rb') as f:
                                    string_data = f.read().decode("utf-8")

                                data = main_options("multiple", xvg, string_data)

                        with st.expander("Labels"):
                            label_options("multiple")

                        with st.expander("Title"):
                            title_options("multiple")

                        with st.expander("Legends"):
                            legend_options("multiple")

                        with st.expander("Axis Multiplication"):
                            axis_multiplication_options("multiple")

                        with st.expander("Data Modifier"):
                            modifier_selector_columns, modifier_columns = modifier_options("multiple", data.shape[0])

                        with st.expander("Axis Limitation"):
                            limit_options("multiple")

                        with st.expander("Opacity"):
                            opacity_options("multiple")

                        if st.button("Plot XVG"):
                            plotting("multiple", data, modifier_selector_columns)

        with wrapper_columns[1]:
            plotter("multiple")

elif selected == "Documentation":
    st.markdown("""
# Introduction

XVG Plotter is a plotting tool for xvg files based on streamlit library.

# Installation

## Anaconda

1. Run create environment command.

```shell
conda env create -f environment.yml # for windows

conda env create -f environment-linux.yml # for linux

conda activate xvg-plotter
```

2. Start streamlit app

```shell
streamlit run main.py
```

The app will be start on port 8501 and you can access by http://localhost:8501.

If you want to run on another port run:

```shell
streamlit run main.py --server.port=7500
```

## Docker

1. Pull latest firesimulations/xvg-plotter image

```shell
docker pull firesimulations/xvg-plotter:latest
```

2. Run docker container

```shell
docker run -p 7500:7500 -d --name xvg-plotter firesimulations/xvg-plotter:latest
```

The app will be start on port 7500 and you can access by http://localhost:7500.

If you want to run on another port run:

```shell
docker run -p 8500:7500 -d --name xvg-plotter firesimulations/xvg-plotter:latest 
```

If you must provide docker volume for running Folder Analysis. For example, if your projects are in C:/projects/md/prod folder pass volume as `-v C:/projects/md/prod:/projects`.

`:/projects` should not be changed. Otherwise, it will show error.

```shell
docker run -p 7500:7500 -d -v C:/projects/md/prod:/projects --name xvg-plotter firesimulations/xvg-plotter:latest
```

# Usage

You can plot XVG file singly or select folder for ease selection.

## Single File Analysis

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/single_01.png" alt="Single File Analysis - Full View" width="100%" height="auto">

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/single_02.png" alt="Single File Analysis - Options" width="100%" height="auto">

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/single_03.png" alt="Single File Analysis - Multi Line" width="100%" height="auto">

### Options

1. File Name: File name for saving. File name will be auto generated up on selected file.
2. Select X Axis: Select X axis from radio button group.
3. Select Y Axis: Select Y axis from multi selection. You can plot multiple lines.
4. Labels:
    * X Label: X axis label. You can give equation by adding $. for example: `Density ($m^3$)`
    * Y Label: X axis label.
    * Label Size: Label font size of X and Y axes. You can select `12` to `24`.
5. Title
    * Show Title: Checkbox for showing title.
    * Title: Auto generated title from XVG file. Then you can update.
    * Title Size: Title font size. You can select `12` to `30`.
    * Title Location: Location of title.
6. Legends:
    * Show Legend: Checkbox for showing legend.
    * Legend Size: Legend font size. You can select `8` to `24`.
    * Legend Location: Location of legend.
7. Plot XVG: Button for plotting.
8. Download Plot: Button for downloading image.

## Folder Analysis

### Options for Running Anaconda:

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/folder_01.png" alt="Folder Analysis - Full View" width="100%" height="auto">

1. Put Project Folder: After copy and pasting project folder path, click Submit button. It will show success or error message after validating the path.
2. Select XVG File: All xvg file in the project folder will be populated here.
3. Other options are same as Single File Analysis.

### Options for Running Docker:

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/folder_02.png" alt="Folder Analysis - Docker Folder Selection" width="100%" height="auto">

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/folder_03.png" alt="Folder Analysis - Docker Folder Selection" width="100%" height="auto">

1. Select Folder: Your passed volume in time of running container will be the root volume. Folders of the root folder will be populated automatically. Hidden folders will be excluded.
2. Action Buttons:
   * Select Button: After selecting a folder click Select Button if the XVG files are in the folder. 
   * Next Button: If XVG files are in child folder, then click Next Button to show children folders.
   * Clear Button: You can clear selection by clicking Clear Button.
3. Select XVG File: All xvg file in the project folder will be populated here.
4. Other options are same as Single File Analysis.
    """, unsafe_allow_html=True)

# st.write(st.session_state)

footer = """<style>
    p {
        margin: 0;
    }
    
    a {
        text-align: center;
    }
    
    a:link, a:visited {
        color: blue;
        background-color: transparent;
        text-decoration: underline;
    }
    
    a:hover, a:active {
        color: red;
        background-color: transparent;
        text-decoration: underline;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
    }
</style>

<div class="footer">
    <p>XVG Plotter, Version 0.11.0</p>
    <p><a href="https://www.linkedin.com/in/dilwarhossain" target="_blank">Dilwar Hossain Noor</a></p>
    <p><a href="https://github.com/bio-grids/xvg-plotter" target="_blank">GitHub</a>, <a href="https://hub.docker.com/r/firesimulations/xvg-plotter" target="_blank">DockerHub</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
