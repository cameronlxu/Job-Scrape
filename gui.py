import PySimpleGUI as sg


def UI() -> list:
    """
        Use GUI to retreive user inputs, return a list of these inputs
    """
    sg.theme('LightBrown1')     # Nice color theme

    layout = [  [sg.Text('Enter a Job Title:'), sg.InputText()],
                [sg.Text('Enter a Zip Code: '), sg.InputText()],
                [sg.Text('How many pages?'), sg.Combo(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])],
                [sg.Button('Generate CSV File')]
    ]

    # Create the Window
    window = sg.Window('Job-Scrape', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    inputs = None
    while True:
        event, values = window.read()

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Generate CSV File':
            # Check if there is a missing input
            if check_valid_inputs(values) == True:
                inputs = values
                break
    window.close()
    return inputs


def check_valid_inputs(values) -> bool:
    """
        Returns boolean on if an empty value is found within user inputs
    """
    for user_input in values:
        if values[user_input] == '':
            sg.Popup('Oops!', 'Looks like there is a missing input!') 
            return False
    return True


if __name__ == "__main__":
    UI()