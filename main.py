import os
from io import StringIO, BytesIO

import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu

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
    None, ["Single File Analysis", "Folder Analysis"],
    icons=['cloud-upload', "list-task"],
    menu_icon="cast", default_index=0, orientation="horizontal"
)

if selected == "Single File Analysis":
    img = BytesIO()

    wrapper_columns = st.columns([3, 2])

    with wrapper_columns[0]:
        with st.form("xvg_form"):
            files = st.columns([3, 2])
            xvg = files[0].file_uploader(label="Upload XVG File", accept_multiple_files=False, type=["xvg"])

            file_name_columns = st.columns([1])
            file_name = file_name_columns[0].text_input(label="File Name")

            label_columns = st.columns([1, 1])
            x_label = label_columns[0].text_input(label="X Label")
            y_label = label_columns[1].text_input(label="Y Label")

            index_columns = st.columns([1, 1])
            x_index = index_columns[0].number_input(label="X Index", min_value=0, max_value=10, step=1)
            y_index = index_columns[1].number_input(label="Y Index", min_value=1, max_value=10, step=1)

            size_columns = st.columns([1])
            label_size = size_columns[0].slider(label="Label Size", min_value=12, max_value=24, step=1, value=16)

            st.form_submit_button('Plot XVG')

            if file_name and x_label and y_label and label_size:
                if xvg is not None:
                    stringio = StringIO(xvg.getvalue().decode("utf-8"))

                    string_data = stringio.read()

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
                    label="Download Graph",
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
                    label="Download Graph",
                    data=img,
                    file_name=f"{file_name}.png",
                    mime="image/png"
                )

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
    <p>XVG Plotter, Version 0.2.0</p>
    <p><a href="https://www.linkedin.com/in/dilwarhossain" target="_blank">Dilwar Hossain Noor</a></p>
    <p><a href="https://github.com/bio-grids/xvg-plotter" target="_blank">GitHub</a>, <a href="https://hub.docker.com/r/firesimulations/xvg-plotter" target="_blank">DockerHub</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
