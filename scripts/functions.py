import streamlit as st
from streamlit_option_menu import option_menu


def colored_widget_block_text(color, content):
    # Apply CSS styling to create a colored widget block
    styled_content = f'<div style="background-color: {color}; padding: 10px; border-radius: 5px;">{content}</div>'
    st.markdown(styled_content, unsafe_allow_html=True)

def colored_widget_block_checkbox(
    color,
    content,
    checkbox_options,
    font_size="16px",
    font_color="black",
    font_style="normal",
):
    # Apply CSS styling to create a colored widget block
    styled_content = f'<div style="background-color: {color}; padding: 10px; border-radius: 5px;">'
    styled_content += f'<p style="font-size: {font_size}; color: {font_color}; font-style: {font_style};">{content}</p>'

    for option in checkbox_options:
        styled_content += f'<input type="checkbox" id="{option}" style="font-size: {font_size}; color: {font_color}; font-style: {font_style};">'
        styled_content += f'<label for="{option}" style="font-size: {font_size}; color: {font_color}; font-style: {font_style};">{option}</label><br>'

    styled_content += "</div>"
    st.markdown(styled_content, unsafe_allow_html=True)


def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Home", "Projects", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Projects", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Overzicht", "Weer & Klimaat", "Methode"],  # required
            icons=["water", "sun", "book"],  # optional
            # menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#fafafa",
                },
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "2px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {
                    "background-color": "#00A9C1",
                    "color": "white",
                },
            },
        )
        return selected



def widget_block(title, text, bg_color):
    """
    Display a widget block with a title, text, and background color.

    Parameters:
        title (str): The title of the block.
        text (str): The text to be displayed inside the block.
        bg_color (str): The background color of the block.

    Returns:
        None
    """
    # Custom CSS for styling the block
    block_style = f"""
        <style>
            .widget-block {{
                padding: 10px;
                border-radius: 5px;
                background-color: {bg_color};
            }}
            .widget-block-title {{
                font-size: larger;
            }}
        </style>
    """

    # Display the widget block
    st.markdown(block_style, unsafe_allow_html=True)
    st.write(f'<div class="widget-block"><div class="widget-block-title">{title}</div>{text}</div>', unsafe_allow_html=True)


def color_selectbox(n_element: int, color: str):
    js = f'''
    <script>
    // Find all the selectboxes
    var selectboxes = window.parent.document.getElementsByClassName("stSelectbox");

    // Select one of them
    var selectbox = selectboxes[{n_element}];

    // Select only the selection div
    var selectregion = selectbox.querySelector('[data-baseweb="select"]');

    // Modify the color
    selectregion.style.backgroundColor = '{color}';
    </script>
    '''
    st.components.v1.html(js, height=0)

#%%

def display_legend(legend_dict, header_title="Legend", icon_class="fas fa-database"):
    #st.text(header_title)
    for category, color in legend_dict.items():
        st.markdown(f'''
            <div style="
                display: inline-flex;
                align-items: center;
                margin-bottom: 5px;
            ">
                <div style="
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background-color: {color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 12px;
                    margin-right: 8px;
                ">
                    <i class="{icon_class}"></i>
                </div>
                <span>{category}</span>
            </div>
        ''', unsafe_allow_html=True)

def display_line_legend(legend_dict, header_title="Legend"):
  #  st.markdown(f"### {header_title}")
    for category, color in legend_dict.items():
        st.markdown(f'''
            <div style="
                display: inline-flex;
                align-items: center;
                margin-bottom: 5px;
            ">
                <div style="
                    width: 20px;
                    height: 2px;
                    background-color: {color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 8px;
                ">
                </div>
                <span>{category}</span>
            </div>
        ''', unsafe_allow_html=True)

def create_custom_box(title, text, icon, background_color="#f0f0f0"):
    # Include the Font Awesome CSS
    font_awesome_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">'
    st.markdown(font_awesome_css, unsafe_allow_html=True)

    st.markdown(f'''
        <div style="
            position: relative;
            background-color: {background_color};
            padding: 20px;
            border-radius: 15px 30px 30px 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        ">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <h3 style="margin: 0;">{title}</h3>
                <div style="
                    width: 25px;
                    height: 25px;
                    border-radius: 50%;
                    background-color: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
                ">
                    <i class="{icon}" style="color: #000000;"></i>
                </div>
            </div>
            <p style="margin-top: 10px;">{text}</p>
        </div>
    ''', unsafe_allow_html=True)

def display_expander_content(locs, df, expander_index, var):
    expander_key = f"expander_{expander_index}"
    if expander_key not in st.session_state:
        st.session_state[expander_key] = False

    expander = st.expander(f"Meetlocatie {expander_index}", expanded=st.session_state[expander_key])

    with expander:
        if st.session_state[expander_key] is False:
            st.session_state[expander_key] = True

        if st.session_state[expander_key]:
            selected_location_name = st.selectbox(f'Selecteer de meetlocatie {expander_index}',
                                                  locs['name'])

            selected_location_code = \
                locs.loc[
                    locs['name'] == selected_location_name, 'code'].iloc[0]

            if var == 'groundwater':
                plot_timeseries_with_percentiles(df, selected_location_code, title=selected_location_name,
                                                 ylabel='Grondwaterniveau (mNAP)')
            else:
                plot_timeseries_with_phases(df, selected_location_code, title=selected_location_name,
                                            ylabel='Afvoer debiet m3/s')


def hover_popup(bold_text, icon_html, popup_text):
    # Define CSS for the hover popup
    hover_popup_css = """
    <style>
    .hover-popup {
        position: relative;
        display: inline-block;
    }

    .hover-popup .popuptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Position the popup above the text */
        left: 50%;
        margin-left: -100px; /* Use half of the width (120/2 = 60), to center the popup */
        opacity: 0;
        transition: opacity 0.3s;
    }

    .hover-popup .popuptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #555 transparent transparent transparent;
    }

    .hover-popup:hover .popuptext {
        visibility: visible;
        opacity: 1;
    }

    /* Add some padding and cursor pointer for the icon */
    .hover-popup i {
        padding: 5px;
        cursor: pointer;
    }

    /* Style for the bold text */
    .bold-text {
        font-weight: bold;
        margin-right: 10px;
    }
    </style>
    """

    # Inject CSS into the Streamlit app
    st.markdown(hover_popup_css, unsafe_allow_html=True)

    # Create the hoverable element with popup info
    hover_element = f"""
    <div class="hover-popup">
        <span class="bold-text">{bold_text}</span>
        {icon_html}
        <div class="popuptext" id="myPopup">{popup_text}</div>
    </div>
    """

    st.markdown(hover_element, unsafe_allow_html=True)
