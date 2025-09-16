# alls_startup_simulator

A little startup program like ALLS from seh-gar.

## Features

- All the steps are customizable as possible. You can change all the text or what to run.

- Compatible with different screen ratios.

## Usage

Just modify a few things in `config.json`.

- **`model`**: The model that will show on the startup screen.

- **`screen`**: The screen that will show on the startup screen.

- **`steps`**: The steps that the startup program will run. Each step is an object with the following properties:
  - **`duration`**: The invertal of time (in seconds) that the step will take to complete.
  - **`description`**: The text that will show on next to the loading icon.
  - **`action`**: The action that you want to perform when on this step. Action should be an illegal Python statement.