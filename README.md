# Lens Price Search Application

This is a desktop application developed using Python and Tkinter to search for lens prices based on various criteria such as company, brand, and specific lens attributes. It interacts with a SQLite database to retrieve and display lens price data in a user-friendly interface.

## Features
- Search lenses by **Company**, **Brand**, and other **Lens attributes** like **Lens Index**, **Coating**, **Type**, and **Price**.
- View search results in an interactive **table (Treeview)**.
- Sort the results by any of the columns in ascending or descending order.
- Dynamic brand selection based on the selected company.
- Responsive user interface with the ability to adjust column widths based on data.

## Requirements

### Python Libraries
This application requires the following Python libraries:
- `tkinter`: For building the graphical user interface (GUI).
- `Pillow`: For loading and displaying images.
- `sqlite3`: For interacting with the SQLite database.

### Installation of Required Libraries
Before running the application, ensure that the necessary libraries are installed using `pip`:
```bash
pip install pillow
```
`tkinter` and `sqlite3` are typically included in standard Python distributions.



## Setup

### 1. Download the source code and place it in a directory on your system.

### 2. Prepare the Database:

The application requires an SQLite database (`data.db`) with a table named `lens_price`. The table should have the following columns:
- `Company`
- `Brand`
- `Lens_Index`
- `Coating`
- `Type`
- `Price`

Ensure that the database is located in the same directory as the application or modify the connection path as needed.

### 3. Add Image Files:

Ensure the following image files are present in the `images` folder:
- `logo.png`: The logo image for the application.
- `search.ico`: The icon used for the application window.

### 4. Run the Application:

You can run the application by executing the Python script `main.py` or by packaging it into a standalone executable using a tool like **PyInstaller**.

## Usage

1. Launch the application.
2. Select a **Company** from the dropdown list. After selecting the company, the brands associated with that company will be displayed in the second dropdown.
3. Select a **Brand** from the dropdown list (optional).
4. Enter a **search term** in the search box to filter the results based on the selected column (e.g., Lens Index, Coating, Type, Price).
5. Click the **"Search"** button to view the filtered results in the table below.
6. The table displays the search results, and you can click on any column header to sort the data in ascending or descending order.

## Code Structure

- **Main GUI**: Built using `tkinter`, with widgets such as labels, buttons, entry fields, and dropdown lists for user interaction.
- **Database Interaction**: The SQLite database is queried using `sqlite3`, and results are displayed dynamically in the `Treeview` widget.
- **Dynamic Content**: The company and brand lists are dynamically populated from the database.

## Known Issues

- **No database found**: The application will raise an error if it cannot connect to the database (`data.db`).
- **Missing images**: If the `logo.png` or `search.ico` images are missing, the application will not run as expected.

## Version

**1.0**  
Developed by **Elhussein Taha**
