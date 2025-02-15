# Fishnet Data Logger (Windows Edition)

This Python script collects data from Fishnet hourly and saves it to a CSV file.

## Description

Fishnet is a network analysis and simulation tool. This script reads data from the `.fishnet-stats` JSON file, which Fishnet automatically generates and updates. This file contains key statistical information about the analyzed network, such as the number of nodes, connections, and other metrics.  The script extracts `total_batches`, `total_positions`, and `total_nodes` from this file, and saves them along with a timestamp in `FishnetCSV1.csv`.

## Prerequisites

-   Windows 10 or later
-   Python 3.x (tested with version 3.9) - <https://www.python.org/downloads/>
-   Fishnet must be installed and configured to generate the `.fishnet-stats` file in the user's home directory (`C:\Users\<Username>\.fishnet-stats`).  Fishnet's documentation should be consulted for details on how to enable and configure statistics generation.
-   Write access to the directory where the CSV file will be created.

## Installation

1.  Install Python (see link above). Select the "Add Python to PATH" option during installation.
2.  Save the script: `FishcountToCSV.py` in a folder of your choice.

## Usage

1.  Open PowerShell.
2.  Navigate to the script: `cd C:\Path\to\Script`.
3.  Run the script: `python FishcountToCSV.py` or `py FishcountToCSV.py`

## Configuration

-   `.fishnet-stats`: Path relative to the user's home directory.
-   `FishnetCSV1.csv`: Name of the CSV file.

## Example

CSV file columns:

-   `Timestamp`: `YYYY-MM-DD HH:MM:SS`
-   `Total Batches`
-   `Total Positions`
-   `Total Nodes`

## Error Handling

-   `FileNotFoundError`: `.fishnet-stats` not found.
-   `JSONDecodeError`: Error reading `.fishnet-stats`.
-   Unexpected errors are displayed.

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

## Contact

Feel free to open an issue on GitHub at ounben (https://github.com/ounben) for any questions or feedback. 
