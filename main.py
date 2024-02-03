import os
import pathlib
from io import StringIO, BytesIO
from pathlib import Path
from typing import Literal, List

import matplotlib.pyplot as plt
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
    None, ["Single File Analysis", "Folder Analysis", "Documentation"],
    icons=['cloud-upload', "list-task", "file-earmark-medical"],
    menu_icon="cast", default_index=0, orientation="horizontal"
)

if selected == "Single File Analysis":
    wrapper_columns = st.columns([3, 2])

    with wrapper_columns[0]:
        with st.container(border=True):
            files = st.columns([1])
            xvg = files[0].file_uploader(label="Upload XVG File", accept_multiple_files=False, type=["xvg"])

            if xvg is not None:
                stringio = StringIO(xvg.getvalue().decode("utf-8"))

                string_data = stringio.read()

                metadata, data = parse_xvg(string_data)

                st.session_state.single_title = metadata["title"]
                st.session_state.single_series = metadata["labels"]["series"]
                st.session_state.single_xaxis = metadata["labels"]["xaxis"]
                st.session_state.single_yaxis = metadata["labels"]["yaxis"]
                st.session_state.single_xvg_file_name = os.path.splitext(xvg.name)[0]

                file_name_columns = st.columns([1])
                file_name_columns[0].text_input(label="File Name", value=st.session_state.single_xvg_file_name,
                                                key="single_file_name")

                axis_columns = st.columns([1, 2])
                x_index_ = axis_columns[0].radio("Select X Axis",
                                                 [st.session_state.single_xaxis] + st.session_state.single_series,
                                                 index=0)
                y_index__ = axis_columns[1].multiselect(
                    'Select Y Axes',
                    [st.session_state.single_xaxis] + st.session_state.single_series,
                    default=([st.session_state.single_xaxis] + st.session_state.single_series)[
                        1 if len(st.session_state.single_series) else 0]
                )

                st.session_state.single_x_index = (
                        [st.session_state.single_xaxis] + st.session_state.single_series).index(
                    x_index_)
                st.session_state.single_yaxes = list(
                    map(lambda z: ([st.session_state.single_xaxis] + st.session_state.single_series).index(z),
                        y_index__))

                with st.expander("Labels"):
                    label_columns = st.columns([1, 1])
                    label_columns[0].text_input(label="X Label", value=st.session_state.single_xaxis,
                                                key="single_xaxis_updated")
                    label_columns[1].text_input(label="Y Label", value=st.session_state.single_yaxis,
                                                key="single_yaxis_updated")

                    size_columns = st.columns([1])
                    size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16,
                                           key="single_label_size")

                with st.expander("Title"):
                    title_columns = st.columns([1, 1, 1])
                    title_columns[0].checkbox(label="Show Title?", key="single_title_show")
                    title_columns[0].text_input(label="Title", value=st.session_state.single_title,
                                                key="single_title_updated")
                    title_columns[1].slider(label="Title Size", min_value=12, max_value=30, step=1, value=20,
                                            key="single_title_size")
                    title_columns[2].selectbox(label="Title Location", key="single_title_loc",
                                               options=["center", "left", "right"], index=0)

                with st.expander("Legends"):
                    legend_columns = st.columns([1, 1, 1])
                    legend_columns[0].checkbox(label="Show Legend?", key="single_legend_show")
                    legend_columns[1].slider(label="Legend Size", min_value=8, max_value=24, step=1, value=12,
                                             key="single_legend_size")
                    legend_columns[2].selectbox(label="Legend Location", key="single_legend_loc",
                                                options=legend_locations,
                                                index=0)

                with st.expander("Axis Multiplication"):
                    multiplier_x_column = st.columns([1, 3, 1])
                    multiplier_x_column[0].checkbox(label="Multiply X Axis?", key="single_multiply_x")
                    multiplier_x_column[1].number_input(label="Multiplication Value", value=1.0000, key="single_x_multiplication_value")
                    with multiplier_x_column[2]:
                        st.text_input("Value", value=st.session_state.single_x_multiplication_value, disabled=True, key="single_x_show_value")

                    multiplier_y_column = st.columns([1, 3, 1])
                    multiplier_y_column[0].checkbox(label="Multiply Y Axis?", key="single_multiply_y")
                    multiplier_y_column[1].number_input(label="Multiplication Value", value=1.0000,
                                                      key="single_y_multiplication_value")
                    with multiplier_y_column[2]:
                        st.text_input("Value", value=st.session_state.single_y_multiplication_value, disabled=True, key="single_y_show_value")

                if st.button("Plot XVG"):
                    if st.session_state.single_file_name and st.session_state.single_xaxis and st.session_state.single_yaxis and st.session_state.single_label_size:
                        for y in st.session_state.single_yaxes:
                            if st.session_state.single_multiply_y:
                                y_multiplier = st.session_state.single_y_multiplication_value
                            else:
                                y_multiplier = 1

                            if st.session_state.single_multiply_x:
                                x_multiplier = st.session_state.single_x_multiplication_value
                            else:
                                x_multiplier = 1

                            plt.plot(data[..., st.session_state.single_x_index] * x_multiplier, data[..., y] * y_multiplier)

                        if st.session_state.single_legend_show:
                            plt.legend(st.session_state.single_series, loc=st.session_state.single_legend_loc,
                                       fontsize=st.session_state.single_legend_size)
                        if st.session_state.single_title_show:
                            plt.title(label=st.session_state.single_title_updated, loc=st.session_state.single_title_loc,
                                      fontdict={"fontsize": st.session_state.single_title_size}, pad=16)
                        plt.xlabel(fr"{st.session_state.single_xaxis_updated}", fontsize=st.session_state.single_label_size)
                        plt.ylabel(fr"{st.session_state.single_yaxis_updated}", fontsize=st.session_state.single_label_size)
                        plt.savefig(st.session_state.single_img, format='png', dpi=600)

                        st.session_state.single_plot_show = True

    with wrapper_columns[1]:
        with st.container(border=True):
            plot_columns = st.columns([2, 1])
            plot_columns[0].subheader("Plot Visualization")

            if st.session_state.single_img and st.session_state.single_file_name and st.session_state.single_plot_show:
                plot_columns[1].download_button(
                    label="Download Plot",
                    data=st.session_state.single_img,
                    file_name=f"{st.session_state.single_file_name}.png",
                    mime="image/png"
                )

                st.pyplot(plt)

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
                    xvg = st.session_state.docker_project_path / st.session_state.multiple_xvg_file_name

                    if xvg is not None:
                        with open(xvg, "rb") as f:
                            string_data = f.read().decode("utf-8")

                        metadata, data = parse_xvg(string_data)

                        st.session_state.multiple_title = metadata["title"]
                        st.session_state.multiple_series = metadata["labels"]["series"]
                        st.session_state.multiple_xaxis = metadata["labels"]["xaxis"]
                        st.session_state.multiple_yaxis = metadata["labels"]["yaxis"]

                    xvg_file_name = os.path.splitext(st.session_state.multiple_xvg_file_name)[0]

                    file_name_columns = st.columns([1])
                    file_name_columns[0].text_input(label="File Name", value=xvg_file_name,
                                                    key="multiple_file_name")

                    axis_columns = st.columns([1, 2])
                    x_index_ = axis_columns[0].radio(
                        "Select X Axis",
                        [st.session_state.multiple_xaxis] + st.session_state.multiple_series,
                        index=0
                    )
                    y_index__ = axis_columns[1].multiselect(
                        'Select Y Axes',
                        [st.session_state.multiple_xaxis] + st.session_state.multiple_series,
                        default=([st.session_state.multiple_xaxis] + st.session_state.multiple_series)[
                            1 if len(st.session_state.multiple_series) else 0]
                    )

                    st.session_state.multiple_x_index = (
                            [st.session_state.multiple_xaxis] + st.session_state.multiple_series).index(
                        x_index_)
                    st.session_state.multiple_yaxes = list(
                        map(lambda z: ([st.session_state.multiple_xaxis] + st.session_state.multiple_series).index(
                            z),
                            y_index__))

                    with st.expander("Labels"):
                        label_columns = st.columns([1, 1])
                        label_columns[0].text_input(label="X Label", value=st.session_state.multiple_xaxis,
                                                    key="multiple_xaxis_updated")
                        label_columns[1].text_input(label="Y Label", value=st.session_state.multiple_yaxis,
                                                    key="multiple_yaxis_updated")

                        size_columns = st.columns([1])
                        size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16,
                                               key="multiple_label_size")

                    with st.expander("Title"):
                        title_columns = st.columns([1, 1, 1])
                        title_columns[0].checkbox(label="Show Title", key="multiple_title_show")
                        title_columns[0].text_input(label="Title", value=st.session_state.multiple_title,
                                                    key="multiple_title_updated")
                        title_columns[1].slider(label="Title Size", min_value=12, max_value=30, step=1, value=20,
                                                key="multiple_title_size")
                        title_columns[2].selectbox(label="Title Location", key="multiple_title_loc",
                                                   options=["center", "left", "right"], index=0)

                    with st.expander("Legends"):
                        legend_columns = st.columns([1, 1, 1])
                        legend_columns[0].checkbox(label="Show Legend", key="multiple_legend_show")
                        legend_columns[1].slider(label="Legend Size", min_value=8, max_value=24, step=1, value=12,
                                                 key="multiple_legend_size")
                        legend_columns[2].selectbox(label="Legend Location", key="multiple_legend_loc",
                                                    options=legend_locations,
                                                    index=0)

                    with st.expander("Axis Multiplication"):
                        multiplier_x_column = st.columns([1, 3, 1])
                        multiplier_x_column[0].checkbox(label="Multiply X Axis?", key="multiple_multiply_x")
                        multiplier_x_column[1].number_input(label="Multiplication Value", value=1.0000,
                                                            key="multiple_x_multiplication_value")
                        with multiplier_x_column[2]:
                            st.text_input("Value", value=st.session_state.multiple_x_multiplication_value,
                                          disabled=True, key="multiple_x_show_value")

                        multiplier_y_column = st.columns([1, 3, 1])
                        multiplier_y_column[0].checkbox(label="Multiply Y Axis?", key="multiple_multiply_y")
                        multiplier_y_column[1].number_input(label="Multiplication Value", value=1.0000,
                                                            key="multiple_y_multiplication_value")
                        with multiplier_y_column[2]:
                            st.text_input("Value", value=st.session_state.multiple_y_multiplication_value,
                                          disabled=True, key="multiple_y_show_value")

                    if st.button("Plot XVG"):
                        if st.session_state.multiple_file_name and st.session_state.multiple_xaxis and st.session_state.multiple_yaxis and st.session_state.multiple_label_size:
                            for y in st.session_state.multiple_yaxes:
                                if st.session_state.multiple_multiply_y:
                                    y_multiplier = st.session_state.multiple_y_multiplication_value
                                else:
                                    y_multiplier = 1

                                if st.session_state.multiple_multiply_x:
                                    x_multiplier = st.session_state.multiple_x_multiplication_value
                                else:
                                    x_multiplier = 1

                                plt.plot(data[..., st.session_state.single_x_index] * x_multiplier, data[..., y] * y_multiplier)

                            if st.session_state.multiple_legend_show:
                                plt.legend(st.session_state.multiple_series,
                                           loc=st.session_state.multiple_legend_loc,
                                           fontsize=st.session_state.multiple_legend_size)
                            if st.session_state.multiple_title_show:
                                plt.title(
                                    label=st.session_state.multiple_title_updated,
                                    loc=st.session_state.multiple_title_loc,
                                    fontdict={"fontsize": st.session_state.multiple_title_size},
                                    pad=16
                                )
                            plt.xlabel(fr"{st.session_state.multiple_xaxis_updated}",
                                       fontsize=st.session_state.multiple_label_size)
                            plt.ylabel(fr"{st.session_state.multiple_yaxis_updated}",
                                       fontsize=st.session_state.multiple_label_size)
                            plt.savefig(st.session_state.multiple_img, format='png', dpi=600)

                            st.session_state.multiple_plot_show = True

        with xvg_columns[1]:
            with st.container(border=True):
                plot_columns = st.columns([2, 1])
                plot_columns[0].subheader("Plot Visualization")

                if st.session_state.multiple_img and st.session_state.multiple_file_name and st.session_state.multiple_plot_show:
                    plot_columns[1].download_button(
                        label="Download Plot",
                        data=st.session_state.multiple_img,
                        file_name=f"{st.session_state.multiple_file_name}.png",
                        mime="image/png"
                    )

                    st.pyplot(plt)

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
                        xvg = os.path.join(st.session_state.multiple_project_folder,
                                           st.session_state.multiple_xvg_file_name)

                        if xvg is not None:
                            with open(xvg, 'rb') as f:
                                string_data = f.read().decode("utf-8")

                            metadata, data = parse_xvg(string_data)

                            st.session_state.multiple_title = metadata["title"]
                            st.session_state.multiple_series = metadata["labels"]["series"]
                            st.session_state.multiple_xaxis = metadata["labels"]["xaxis"]
                            st.session_state.multiple_yaxis = metadata["labels"]["yaxis"]

                        xvg_file_name = os.path.splitext(st.session_state.multiple_xvg_file_name)[0]

                        file_name_columns = st.columns([1])
                        file_name_columns[0].text_input(label="File Name", value=xvg_file_name,
                                                        key="multiple_file_name")

                        axis_columns = st.columns([1, 2])
                        x_index_ = axis_columns[0].radio("Select X Axis",
                                                         [
                                                             st.session_state.multiple_xaxis] + st.session_state.multiple_series,
                                                         index=0)
                        y_index__ = axis_columns[1].multiselect(
                            'Select Y Axes',
                            [st.session_state.multiple_xaxis] + st.session_state.multiple_series,
                            default=([st.session_state.multiple_xaxis] + st.session_state.multiple_series)[
                                1 if len(st.session_state.multiple_series) else 0]
                        )

                        st.session_state.multiple_x_index = (
                                [st.session_state.multiple_xaxis] + st.session_state.multiple_series).index(
                            x_index_)
                        st.session_state.multiple_yaxes = list(
                            map(lambda z: ([st.session_state.multiple_xaxis] + st.session_state.multiple_series).index(
                                z),
                                y_index__))

                        with st.expander("Labels"):
                            label_columns = st.columns([1, 1])
                            label_columns[0].text_input(label="X Label", value=st.session_state.multiple_xaxis,
                                                        key="multiple_xaxis_updated")
                            label_columns[1].text_input(label="Y Label", value=st.session_state.multiple_yaxis,
                                                        key="multiple_yaxis_updated")

                            size_columns = st.columns([1])
                            size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16,
                                                   key="multiple_label_size")

                        with st.expander("Title"):
                            title_columns = st.columns([1, 1, 1])
                            title_columns[0].checkbox(label="Show Title", key="multiple_title_show")
                            title_columns[0].text_input(label="Title", value=st.session_state.multiple_title,
                                                        key="multiple_title_updated")
                            title_columns[1].slider(label="Title Size", min_value=12, max_value=30, step=1, value=20,
                                                    key="multiple_title_size")
                            title_columns[2].selectbox(label="Title Location", key="multiple_title_loc",
                                                       options=["center", "left", "right"], index=0)

                        with st.expander("Legends"):
                            legend_columns = st.columns([1, 1, 1])
                            legend_columns[0].checkbox(label="Show Legend", key="multiple_legend_show")
                            legend_columns[1].slider(label="Legend Size", min_value=8, max_value=24, step=1, value=12,
                                                     key="multiple_legend_size")
                            legend_columns[2].selectbox(label="Legend Location", key="multiple_legend_loc",
                                                        options=legend_locations,
                                                        index=0)

                        with st.expander("Axis Multiplication"):
                            multiplier_x_column = st.columns([1, 3, 1])
                            multiplier_x_column[0].checkbox(label="Multiply X Axis?", key="multiple_multiply_x")
                            multiplier_x_column[1].number_input(label="Multiplication Value", value=1.0000,
                                                                key="multiple_x_multiplication_value")
                            with multiplier_x_column[2]:
                                st.text_input("Value", value=st.session_state.multiple_x_multiplication_value,
                                              disabled=True, key="multiple_x_show_value")

                            multiplier_y_column = st.columns([1, 3, 1])
                            multiplier_y_column[0].checkbox(label="Multiply Y Axis?", key="multiple_multiply_y")
                            multiplier_y_column[1].number_input(label="Multiplication Value", value=1.0000,
                                                                key="multiple_y_multiplication_value")
                            with multiplier_y_column[2]:
                                st.text_input("Value", value=st.session_state.multiple_y_multiplication_value,
                                              disabled=True, key="multiple_y_show_value")

                        if st.button("Plot XVG"):
                            if st.session_state.multiple_file_name and st.session_state.multiple_xaxis and st.session_state.multiple_yaxis and st.session_state.multiple_label_size:
                                for y in st.session_state.multiple_yaxes:
                                    if st.session_state.multiple_multiply_y:
                                        y_multiplier = st.session_state.multiple_y_multiplication_value
                                    else:
                                        y_multiplier = 1

                                    if st.session_state.multiple_multiply_x:
                                        x_multiplier = st.session_state.multiple_x_multiplication_value
                                    else:
                                        x_multiplier = 1

                                    plt.plot(data[..., st.session_state.single_x_index] * x_multiplier, data[..., y] * y_multiplier)

                                if st.session_state.multiple_legend_show:
                                    plt.legend(st.session_state.multiple_series,
                                               loc=st.session_state.multiple_legend_loc,
                                               fontsize=st.session_state.multiple_legend_size)
                                if st.session_state.multiple_title_show:
                                    plt.title(
                                        label=st.session_state.multiple_title_updated,
                                        loc=st.session_state.multiple_title_loc,
                                        fontdict={"fontsize": st.session_state.multiple_title_size},
                                        pad=16
                                    )
                                plt.xlabel(fr"{st.session_state.multiple_xaxis_updated}",
                                           fontsize=st.session_state.multiple_label_size)
                                plt.ylabel(fr"{st.session_state.multiple_yaxis_updated}",
                                           fontsize=st.session_state.multiple_label_size)
                                plt.savefig(st.session_state.multiple_img, format='png', dpi=600)

                                st.session_state.multiple_plot_show = True

        with wrapper_columns[1]:
            with st.container(border=True):
                plot_columns = st.columns([2, 1])
                plot_columns[0].subheader("Plot Visualization")

                if st.session_state.multiple_img and st.session_state.multiple_file_name and st.session_state.multiple_plot_show:
                    plot_columns[1].download_button(
                        label="Download Plot",
                        data=st.session_state.multiple_img,
                        file_name=f"{st.session_state.multiple_file_name}.png",
                        mime="image/png"
                    )

                    st.pyplot(plt)

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
    <p>XVG Plotter, Version 0.5.0</p>
    <p><a href="https://www.linkedin.com/in/dilwarhossain" target="_blank">Dilwar Hossain Noor</a></p>
    <p><a href="https://github.com/bio-grids/xvg-plotter" target="_blank">GitHub</a>, <a href="https://hub.docker.com/r/firesimulations/xvg-plotter" target="_blank">DockerHub</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
