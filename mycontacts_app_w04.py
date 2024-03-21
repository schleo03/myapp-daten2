import streamlit as st
import pandas as pd
from datetime import date
from github_contents import GithubContents

# Set constants
DATA_FILE = "MyContactsTable.csv"
DATA_COLUMNS = ["Name", "Strasse", "PLZ", "Ort", "Geburtsdatum"]

# Set page configuration
st.set_page_config(page_title="My Contacts", page_icon="🎂", layout="wide",  
                   initial_sidebar_state="expanded")

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def add_entry_in_sidebar():
    """Add a new entry to the DataFrame using pd.concat and calculate age."""
    new_entry = {
        DATA_COLUMNS[0]:  st.sidebar.text_input(DATA_COLUMNS[0]),  # Name
        DATA_COLUMNS[1]:  st.sidebar.text_input(DATA_COLUMNS[1]),  # Strasse
        DATA_COLUMNS[2]:  st.sidebar.text_input(DATA_COLUMNS[2]),  # PLZ
        DATA_COLUMNS[3]:  st.sidebar.text_input(DATA_COLUMNS[3]),  # Ort
        DATA_COLUMNS[4]:  st.sidebar.date_input(DATA_COLUMNS[4],
                                                min_value=date(1950, 1, 1),
                                                format="DD.MM.YYYY"),  # Geburtsdatum
    } 

    # check wether all data is defined, otherwise show an error message
    for key, value in new_entry.items():
        if value == "":
            st.sidebar.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.sidebar.button("Add"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)

        # Save the updated DataFrame to GitHub
        name = new_entry[DATA_COLUMNS[0]]
        msg = f"Add contact '{name}' to the file {DATA_FILE}"
        st.session_state.github.write_df(DATA_FILE, st.session_state.df, msg)

def display_dataframe():
    """Display the DataFrame in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("No data to display.")

def main():
    st.title("Mein Kontakte-App 🎂 (Woche 4)")
    init_github()
    init_dataframe()
    add_entry_in_sidebar()
    display_dataframe()

if __name__ == "__main__":
    main()
