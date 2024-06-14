# Function to show spinner
def show_spinner(spinner, spinner_event):
    spinner.start()
    while not spinner_event.is_set():
        pass
    spinner.stop()