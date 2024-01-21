import os
from io import StringIO, BytesIO

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
if "single_title_size" not in st.session_state:
    st.session_state.single_title_size = 20
if "single_title_show" not in st.session_state:
    st.session_state.single_title_show = False
if "single_title_loc" not in st.session_state:
    st.session_state.single_title_loc = "center"
if "single_xaxis" not in st.session_state:
    st.session_state.single_xaxis = None
if "single_yaxis" not in st.session_state:
    st.session_state.single_yaxis = None
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
        files = st.columns([1])
        xvg = files[0].file_uploader(label="Upload XVG File", accept_multiple_files=False, type=["xvg"])

        if xvg is not None:
            stringio = StringIO(xvg.getvalue().decode("utf-8"))

            string_data = stringio.read()

            file_lines = string_data.split("\n")

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
                                         [st.session_state.single_xaxis] + st.session_state.single_series, index=0)
        y_index__ = axis_columns[1].multiselect(
            'Select Y Axes',
            [st.session_state.single_xaxis] + st.session_state.single_series,
            default=([st.session_state.single_xaxis] + st.session_state.single_series)[
                1 if len(st.session_state.single_series) else 0]
        )

        st.session_state.single_x_index = ([st.session_state.single_xaxis] + st.session_state.single_series).index(
            x_index_)
        st.session_state.single_yaxes = list(
            map(lambda z: ([st.session_state.single_xaxis] + st.session_state.single_series).index(z), y_index__))

        with st.expander("Labels"):
            label_columns = st.columns([1, 1])
            label_columns[0].text_input(label="X Label", key="single_xaxis")
            label_columns[1].text_input(label="Y Label", key="single_yaxis")

            size_columns = st.columns([1])
            size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16,
                                   key="single_label_size")

        with st.expander("Title"):
            title_columns = st.columns([1, 1, 1])
            title_columns[0].checkbox(label="Show Title", key="single_title_show")
            title_columns[0].text_input(label="Title", key="single_title")
            title_columns[1].slider(label="Title Size", min_value=12, max_value=30, step=1, value=20,
                                    key="single_title_size")
            title_columns[2].selectbox(label="Title Location", key="single_title_loc",
                                       options=["center", "left", "right"], index=0)

        with st.expander("Legends"):
            legend_columns = st.columns([1, 1, 1])
            legend_columns[0].checkbox(label="Show Legend", key="single_legend_show")
            legend_columns[1].slider(label="Legend Size", min_value=8, max_value=24, step=1, value=12,
                                     key="single_legend_size")
            legend_columns[2].selectbox(label="Legend Location", key="single_legend_loc", options=legend_locations,
                                        index=0)

        if st.button("Plot XVG"):
            if st.session_state.single_file_name and st.session_state.single_xaxis and st.session_state.single_yaxis and st.session_state.single_label_size:
                for y in st.session_state.single_yaxes:
                    plt.plot(data[..., st.session_state.single_x_index], data[..., y])

                if st.session_state.single_legend_show:
                    plt.legend(st.session_state.single_series, loc=st.session_state.single_legend_loc,
                               fontsize=st.session_state.single_legend_size)
                if st.session_state.single_title_show:
                    plt.title(label=st.session_state.single_title, loc=st.session_state.single_title_loc,
                              fontdict={"fontsize": st.session_state.single_title_size}, pad=16)
                plt.xlabel(fr"{st.session_state.single_xaxis}", fontsize=st.session_state.single_label_size)
                plt.ylabel(fr"{st.session_state.single_yaxis}", fontsize=st.session_state.single_label_size)
                plt.savefig(st.session_state.single_img, format='png', dpi=600)

    with wrapper_columns[1]:
        with st.container(border=True):
            if st.session_state.single_img and st.session_state.single_file_name:
                st.download_button(
                    label="Download Plot",
                    data=st.session_state.single_img,
                    file_name=f"{st.session_state.single_file_name}.png",
                    mime="image/png"
                )

                st.pyplot(plt)

elif selected == "Folder Analysis":
    img = BytesIO()
    file_name = ''

    wrapper_columns = st.columns([3, 2])

    with wrapper_columns[0]:
        xvg_files = []

        with st.container(border=True):
            with st.form("folder_selection_form"):
                folder_columns = st.columns([3, 2])

                with folder_columns[0]:
                    project_folder = st.text_input("Put Project Folder")
                    st.form_submit_button("Submit")
                with folder_columns[1]:
                    if project_folder:
                        st.write(f"Selected folder: {project_folder}")
                        is_exist = os.path.exists(project_folder)
                        if is_exist:
                            st.success("Project folder selected.")
                        else:
                            st.error("This is not a valid folder")

                plotter_folder = os.path.join(project_folder, "xvg-plotter")

                if not os.path.isdir(plotter_folder):
                    os.makedirs(plotter_folder)

                if project_folder:
                    xvg_files = [f for f in os.listdir(project_folder) if
                                 f.endswith(".xvg") and os.path.isfile(os.path.join(project_folder, f))]

            if xvg_files:
                # with st.form("xvg_submit_form"):
                xvg_file = st.selectbox("Select XVG File", options=xvg_files)

                if xvg_file:
                    xvg = os.path.join(project_folder, xvg_file)

                    xvg_file_name = os.path.splitext(xvg_file)[0]

                    file_name_columns = st.columns([1])
                    file_name = file_name_columns[0].text_input(label="File Name", value=xvg_file_name)

                    label_columns = st.columns([1, 1])
                    x_label = label_columns[0].text_input(label="X Label")
                    y_label = label_columns[1].text_input(label="Y Label")

                    index_columns = st.columns([1, 1])
                    x_index = index_columns[0].number_input(label="X Index", min_value=0, max_value=10, step=1)
                    y_index = index_columns[1].number_input(label="Y Index", min_value=1, max_value=10, step=1)

                    size_columns = st.columns([1])
                    label_size = size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1,
                                                        value=16)

                    if st.button("Plot XVG"):
                        if file_name and x_label and y_label and label_size:
                            if xvg is not None:
                                with open(xvg, 'rb') as f:
                                    string_data = f.read().decode("utf-8")

                                # stringio = StringIO(xvg.getvalue().decode("utf-8"))

                                # string_data = stringio.read()

                                file_lines = string_data.split("\n")

                                x = [float(line.split()[int(x_index)]) for line in file_lines if
                                     line and not (line.startswith('#') or line.startswith('@'))]
                                y = [float(line.split()[int(y_index)]) / 1000 for line in file_lines if
                                     line and not (line.startswith('#') or line.startswith('@'))]

                                plt.plot(x, y)
                                plt.xlabel(fr"{x_label}", fontsize=label_size)
                                plt.ylabel(fr"{y_label}", fontsize=label_size)
                                plt.savefig(img, format='png', dpi=600)

    with wrapper_columns[1]:
        with st.container(border=True):
            if img and file_name:
                st.pyplot(plt)

                btn = st.download_button(
                    label="Download Plot",
                    data=img,
                    file_name=f"{file_name}.png",
                    mime="image/png"
                )

elif selected == "Documentation":
    st.markdown("""
# Usage

You can plot XVG file singly or select folder for ease selection.

## Single File Analysis

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/03.png" alt="Single File Analysis - Full View" width="100%" height="auto">

### Options

1. File Name: File name for saving
2. Select X Axis: Select X axis from radio button group.
3. Select Y Axis: Select Y axis from radio button group.
4. X Label: X axis label. You can give equation by adding \$. for example: `Density ($m^3$)`
5. Y Label: X axis label.
6. Label Size: Label font size of X and Y axes. You can select `12` to `24`.
7. Plot XVG: Button for plotting.
8. Download Plot: Button for downloading image.

## Folder Analysis

<img src="https://github.com/bio-grids/xvg-plotter/raw/master/images/02.png" alt="Folder Analysis - Full View" width="100%" height="auto">

### Options

1. Put Project Folder: After copy and pasting project folder path, click Submit button. It will show success or error message after validating the path.
2. Select XVG File: All xvg file in the project folder will be populated here.
3. Other options are same as Single File Analysis.
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
    <p>XVG Plotter, Version 0.3.0</p>
    <p><a href="https://www.linkedin.com/in/dilwarhossain" target="_blank">Dilwar Hossain Noor</a></p>
    <p><a href="https://github.com/bio-grids/xvg-plotter" target="_blank">GitHub</a>, <a href="https://hub.docker.com/r/firesimulations/xvg-plotter" target="_blank">DockerHub</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
