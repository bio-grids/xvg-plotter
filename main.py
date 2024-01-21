import os
from io import StringIO, BytesIO

import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu

from utils import parse_xvg

st.set_page_config(layout="wide", page_title="XVG Plotter")

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
    img = BytesIO()
    file_name = ""
    title = ""
    xaxis = ""
    series = []
    xvg_file_name = ""

    wrapper_columns = st.columns([3, 2])

    with wrapper_columns[0]:
        # with st.form("xvg_form"):
        files = st.columns([3, 2])
        xvg = files[0].file_uploader(label="Upload XVG File", accept_multiple_files=False, type=["xvg"])

        if xvg is not None:
            stringio = StringIO(xvg.getvalue().decode("utf-8"))

            string_data = stringio.read()

            file_lines = string_data.split("\n")

            metadata, data = parse_xvg(string_data)

            # print(data.shape)
            # print(metadata["title"])
            # print(metadata["labels"]["series"])

            title = metadata["title"]
            series = metadata["labels"]["series"]
            xaxis = metadata["labels"]["xaxis"]
            xvg_file_name = os.path.splitext(xvg.name)[0]

        file_name_columns = st.columns([1])
        file_name = file_name_columns[0].text_input(label="File Name", value=xvg_file_name)

        axis_columns = st.columns([1, 1])
        x_index_ = axis_columns[0].radio("Select X Axis", [xaxis] + series, index=0)
        # y_index_ = axis_columns[1].multiselect(
        #     'Select Y Axes',
        #     ["Time"] + series,
        # )
        y_index_ = axis_columns[1].radio("Select Y Axis", [xaxis] + series, index=0)

        label_columns = st.columns([1, 1])
        x_label = label_columns[0].text_input(label="X Label", value=x_index_)
        y_label = label_columns[1].text_input(label="Y Label", value=y_index_)

        x_index = ([xaxis] + series).index(x_index_)
        y_index = ([xaxis] + series).index(y_index_)

        size_columns = st.columns([1])
        label_size = size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16)

        if st.button("Plot XVG"):
            if file_name and x_label and y_label and label_size:
                x = data[..., x_index]
                y = data[..., y_index]

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
