import streamlit as st
import markdown
from lib.main import main
from lib.notification_handler import CustomNotificationHandler
from lib.flight_retriever import FlightRetriever
from lib.config import Config
import time

# Function to read and display the log file content
def display_log_content():
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.read()

        # Display the content of the log file
        st.markdown('**Log File Content:**')
        st.code(log_content)

        # Search for the desired log entry
        if "[notification_handler]:" in log_content:
            log_lines = log_content.split("\n")
            for line in log_lines:
                if "[notification_handler]:" in line:
                    log_entry = line[line.index("[notification_handler]:") + len("[notification_handler]:"):]
                    st.markdown('**Desired Log Entry:**')
                    st.code(log_entry.strip())
                    break

    except Exception as e:
        st.write(f'An error occurred while reading the log file: {str(e)}')

# Function to search for the specified log entry in real-time
def search_log_realtime():
    while search_realtime:
        try:
            with open(log_file_path, 'r') as file:
                log_content = file.read()

            # Search for the specified log entry
            if "[notification_handler]:" in log_content:
                log_lines = log_content.split("\n")
                for line in log_lines:
                    if "[notification_handler]:" in line:
                        log_entry = line[line.index("[notification_handler]:") + len("[notification_handler]:"):]
                        st.markdown('**Real-time Log Entry Found:**')
                        st.code(log_entry.strip())
                        return

        except Exception as e:
            st.write(f'An error occurred while reading the log file: {str(e)}')

        time.sleep(10)

# Create an instance of NotificationHandler and pass the flight_retriever instance to it
log_file_path = "logs/auto-southwest-check-in.log"
config = Config()
flight_retriever = FlightRetriever(config)
notification_handler = CustomNotificationHandler(flight_retriever)

# Add logo and title to sidebar
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="data:image/svg+xml,%3Csvg fill='%23304CB2' role='img' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Ctitle%3ESouthwest Airlines%3C/title%3E%3Cpath d='M22.163 2.419C21.038 1.219 19.35.58 17.437.58c-2.062 0-3.637.675-4.725 1.275 2.063 1.163 6.526 3.75 11.175 7.163.075-.45.113-.938.113-1.388-.038-2.175-.675-4.012-1.837-5.212zm1.35 8.212C18.186 6.244 15 4.031 11.55 1.97 10.612 1.406 8.775.58 6.675.58 4.688.581 3 1.22 1.837 2.42 1.087 3.206.563 4.18.262 5.38 3 7.294 10.462 12.656 18 18.581c2.512-2.362 4.613-5.1 5.512-7.95zM0 7.781c0 6.15 6.487 11.85 12 15.638 1.575-1.088 3.225-2.325 4.8-3.713A736.871 736.871 0 0 0 .15 6.131C.038 6.62 0 7.181 0 7.781Z'/%3E%3C/svg%3E" alt="Logo" width="30">
        <h2 style="margin-left: 10px;">Southwest Checker Inner</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.title('Southwest Check-in Status')
st.markdown('----')

# Sidebar inputs
confirmation_number = st.sidebar.text_input('Confirmation Number')
first_name = st.sidebar.text_input('First Name')
last_name = st.sidebar.text_input('Last Name')

# Checkbox to show log
show_log = st.sidebar.checkbox('Show Log')

# Checkbox for real-time log search
search_realtime = st.sidebar.checkbox('Real Time')

# Button to start the script
if st.sidebar.button('Run Checkin'):
    if confirmation_number and first_name and last_name:
        st.markdown('Running the check-in process...')
        arguments = [confirmation_number, first_name, last_name, "--verbose"]
        st.write(arguments)
        try:
            output = main(arguments)
            st.markdown('Check-in process completed.')

            # Display output in the main page
            st.write(f'Output:\n{output}')

            # If the success phrases are in the output, display them at the top
            success_phrases = ["Successfully scheduled the following flights to check in for", "Flight from"]
            for phrase in success_phrases:
                if phrase in output:
                    st.markdown(f"**{phrase}**")

            # Refresh log file content
            display_log_content()

        except Exception as e:
            st.write(f'An error occurred: {str(e)}')

    else:
        st.sidebar.warning('Please input all required fields')

# Button to refresh the log file content
if st.button('Refresh Log'):
    display_log_content()

# Real-time log search
if search_realtime:
    search_log_realtime()

# Display log file content if the checkbox is checked
if show_log:
    display_log_content()
