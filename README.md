# AE Compensation Dashboard

This project provides a comprehensive dashboard for analyzing and visualizing Account Executive (AE) compensation, including their base salary, variable components, and accelerators. Below are the instructions for setting up and running the project locally.

---

## Prerequisites

1. **Python:** Ensure you have Python 3.8 or later installed. You can download it from [python.org](https://www.python.org/).
2. **Git:** Make sure Git is installed for version control.
3. **Virtual Environment (optional):** It is recommended to use a virtual environment to manage dependencies.

---

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Replace `<repository-url>` with the URL of your Git repository.

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use env\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Prepare Data Files (optional)

Ensure the data files are in the correct location as required by the project. For example, place the `compensationModelTaskData.xlsx` file in the `data/` folder.

---

## Running the Project

1. **Start the Application:**

Run the following command to start the Dash application:

```bash
python app.py
```

2. **Access the Dashboard:**

Open your browser and go to:

```
http://127.0.0.1:8050
```

---

## Key Features

- **Compensation Analysis:** Breakdown of total compensation, including base salary, upsells, new logos, services, and accelerators.
- **Interactive Visualizations:** Dynamic bar charts, heatmaps, and other visualizations.
- **Filters:** Filter data by year and month to analyze compensation trends.
- **Export Data:** Download AE compensation and global summary data as CSV.

---

## Project Structure

- **`app.py`**: The main entry point of the application.
- **`pages/`**: Contains modular layouts and callbacks for individual pages.
- **`components/`**: Reusable components like navigation bars and cards.
- **`data/`**: Folder for input datasets.
- **`compensation_model/`**: Contains the logic for calculating compensation.
- **`assets/`**: Contains CSS and other static files.

---

## Troubleshooting

1. **Dependencies Issue:**
   If you encounter issues with package installation, ensure your `pip` is updated:
   ```bash
   pip install --upgrade pip
   ```

2. **Port Already in Use:**
   If port 8050 is already in use, run the application on a different port:
   ```bash
   python app.py --port 8060
   ```

3. **Data File Missing:**
   Ensure the required data files are placed in the correct directory (e.g., `data/compensationModelTaskData.xlsx`).

---

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Ensure to follow the project's code style and guidelines.

---


