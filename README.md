# alls_startup_simulator

A little startup program like ALLS from seh-gar.

## Features

- All the steps are customizable as possible. You can change all the text or what to run.

- Support calling out an error screen.

- Compatible with different screen ratios.

## Usage

Just modify a few things in `config.json`.

- **`model`**: The model that will show on the startup screen.

- **`screen`**: The screen that will show on the startup screen.

- **`background_color`**: The background color of the startup screen.

- **`font_color`**: The color of the text on the screen.

- **`steps`**: The steps that the startup program will run. Each step is an object with the following properties:
  - **`duration`**: The interval of time (in seconds) that the step will take to complete.
  - **`description`**: The text that will show on next to the loading icon.
  - **`action`**: The action that you want to perform when on this step. Action should be an legal Python statement.

- **`errors`**: The errors that will show when the `action` in `step` call out an error. Each error number and description follows a key-value pair format.
  - Key: The error number.
  - Value: The error description.

- When error was defined in `errors`, you can run `error('Error Number Here')` in `action` to call out an error.
  - Don't forget to make the error number in string. For example: `"action": "error('0001')"`