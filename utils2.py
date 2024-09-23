import streamlit as st
import base64
from streamlit.components.v1 import html
from SETTINGS import *

def inject_custom_css():
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_current_route():
    try:
        nav_param = st.query_params.nav
        if nav_param is None or nav_param == 'uitloggen':
            nav_param = 'invullen'
            st.query_params.nav = 'invullen'
        return nav_param

    except:
        if "nav" not in st.query_params.to_dict():
            st.query_params.nav = 'invullen'

def navbar_authenticated(name, title=TITLE, logo_path=LOGO_PATH,nav_bool=NAV_BOOL):
    with open(logo_path, "rb") as image_file:
        image_as_base64 = base64.b64encode(image_file.read())

    current_route = get_current_route()

    if nav_bool == True:
        navbar_items = ''
        for key, value in NAVBAR_PATHS.items():
            if value == current_route:
                navbar_items += (f'<a class="navitem active" href="/?nav={value}" target="_self">{key}</a>')
            else:
                navbar_items += (f'<a class="navitem" href="/?nav={value}" target="_self">{key}</a>')

        settings_items = ''
        for key, value in SETTINGS.items():
            settings_items += (f'<a href="/?nav={value}" class="settingsNav" target="_self">{key}</a>')

        component = rf'''
        <nav class="container navbar" id="navbar">
            <img class="navbar-logo" src="data:image/png;base64, {image_as_base64.decode("utf-8")}" style="width: 35px; height: 35;">
            <ul class="navlist">    
                {navbar_items}
            </ul>            
            <p class="navbar-text-center">{title}</p>
            <div class="dropdown" id="settingsDropDown">
                <button class="dropbtn">Hi {name} ↓</button>
                <div class="dropdown-content" id="myDropdown">
                    {settings_items}
                </div>
            </div>
        </nav>
        '''

        st.markdown(
        """
            <style>
                .appview-container .main .block-container {{
                    padding-top: {padding_top}rem;
                    padding-bottom: {padding_bottom}rem;
                    }}
                    st.markdown(
    
                }}
            unsafe_allow_html=True,
        )
            </style>""".format(
            padding_top=0, padding_bottom=0
        ),
        unsafe_allow_html=True,
    )
        st.markdown(component, unsafe_allow_html=True)
        js = '''
        <script>        
            // Dropdown hide / show
            var dropdown = window.parent.document.getElementById("settingsDropDown");
            dropdown.onclick = function() {
                var dropWindow = window.parent.document.getElementById("myDropdown");
                if (dropWindow.style.visibility == "hidden"){
                    dropWindow.style.visibility = "visible";
                }else{
                    dropWindow.style.visibility = "hidden";
                }
            };
        
        </script>
        '''
        html(js,height=0)


    else:
        settings_items = ''
        for key, value in SETTINGS.items():
            settings_items += (f'<a href="/?nav={value}" class="settingsNav" target="_self">{key}</a>')

        component = rf'''
            <nav class="container navbar" id="navbar">
                <img class="navbar-logo" src="data:image/png;base64, {image_as_base64.decode("utf-8")}" style="width: 35px; height: 35;">
                <p class="navbar-text-center">{title}</p>
                <div class="dropdown" id="settingsDropDown">
                    <button class="dropbtn">Welkom {name} ↓</button>
                    <div class="dropdown-content" id="myDropdown">
                        {settings_items}
                    </div>
                </div>
            </nav>
            '''

        st.markdown(
            """
                <style>
                    .appview-container .main .block-container {{
                        padding-top: {padding_top}rem;
                        padding-bottom: {padding_bottom}rem;
                        }}
                        st.markdown(

                    }}
                unsafe_allow_html=True,
            )
                </style>""".format(
                padding_top=0, padding_bottom=0
            ),
            unsafe_allow_html=True,
        )
        st.markdown(component, unsafe_allow_html=True)
        js = '''
            <script>        
                // Dropdown hide / show
                var dropdown = window.parent.document.getElementById("settingsDropDown");
                dropdown.onclick = function() {
                    var dropWindow = window.parent.document.getElementById("myDropdown");
                    if (dropWindow.style.visibility == "hidden"){
                        dropWindow.style.visibility = "visible";
                    }else{
                        dropWindow.style.visibility = "hidden";
                    }
                };

            </script>
            '''
        html(js, height=0)
        bottom_navbar = rf'''
        <nav class="bottom-navbar">
            <a class="navitem {"active" if st.query_params.nav == "invullen" or st.query_params.nav is None else ""}" href="/?nav=invullen " target="_self">Invullen</a>
            <a class="navitem {"active" if st.query_params.nav == "overzicht" else ""}" href="/?nav=overzicht" target="_self">Overzicht</a>
        </nav>
        '''
        st.markdown(bottom_navbar, unsafe_allow_html=True)



def navbar_unauthenticated(title=TITLE,logo_path= LOGO_PATH):
    with open(logo_path, "rb") as image_file:
        image_as_base64 = base64.b64encode(image_file.read())

    component = rf'''
    <nav class="container navbar" id="navbar">
        <img class="navbar-logo" src="data:image/png;base64, {image_as_base64.decode("utf-8")}" style="width: 35px; height: 35px;">
        <p class="navbar-text-center">{TITLE}</p>
    </nav>
    '''
    st.markdown(
    """
        <style>
            .appview-container .main .block-container {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                }}

        </style>""".format(
        padding_top=0, padding_bottom=0
    ),
    unsafe_allow_html=True,
)
    st.markdown(component, unsafe_allow_html=True)