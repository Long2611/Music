# Music
Final Project for COMP705 Full Stack Development

# Music Environment Activation

This repository contains scripts to activate the `musicvenv` Conda environment on both Windows and macOS.

## Scripts

- `activate_env.bat`: Script for activating the environment on Windows.
- `activate_env.sh`: Script for activating the environment on macOS.

## Usage

### Windows

1. Double-click on `activate_env.bat` to activate the `musicvenv` environment.
   - Alternatively, you can right-click on `activate_env.bat` and select "Run as administrator" if necessary.
   - Alternatively, run the command `activate_env.bat` in a Command Prompt window.

### macOS

1. Open a terminal and navigate to the directory containing `activate_env.sh`.
2. Run the following command to make the script executable:
   ```bash
   chmod +x activate_env.sh
   ```

### creating the environment:
Run the following command to create the environment if the scripts are not loading properly.
```conda env export > env.yml```
