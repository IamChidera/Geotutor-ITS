# GeoTutor ITS – Intelligent Tutoring System

A fully adaptive, multi-user Intelligent Tutoring System (ITS) for teaching geometric area calculations. Built with Python, Tkinter, OWL ontologies, and Bayesian Knowledge Tracing.

## 🎯 Features

- **Multi-User Support**: Individual student profiles with persistent mastery tracking
- **Adaptive Difficulty**: Automatically adjusts problem difficulty (easy/medium/hard) based on student performance
- **Bayesian Knowledge Tracing (BKT)**: Probabilistic mastery model that tracks learning progress
- **Random Problem Generation**: Unlimited unique problems for each shape type
- **Ontology-Based Expert Model**: OWL ontology (`GeoTutor.owl`) with SWRL rules for area calculations
- **Visual Feedback**: Real-time shape visualizations and mastery progress bars
- **Worked Examples**: Step-by-step examples for each shape type
- **Student → Resource Mapping**: Ontology links students to learning resources (shapes)

## 📋 Prerequisites

- **Python 3.8+**
- **Java** (optional, only needed if using Pellet/HermiT reasoner with ontology)
- Required Python packages (see `requirements.txt`)

## 🚀 Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Generate the ontology** (if not already present):
   ```bash
   python generate_owl.py
   ```
   Or use the extended version:
   ```bash
   python new_generate_owl.py
   ```

## 🎮 Usage

### Running the Application

```bash
python geotutor_main.py
```

1. **Login**: Enter your Student ID when prompted (e.g., `202300123`)
2. **Select Shape**: Choose Triangle, Square, or Rectangle
3. **View Problem**: The system generates a random problem at your current difficulty level
4. **Enter Answer**: Type your calculated area in the answer field
5. **Check Answer**: Click "Check Answer" or press Enter
6. **Get Feedback**: Receive immediate feedback and adaptive difficulty adjustment

### Features in Action

- **Correct Answer**: Mastery increases, difficulty may advance (easy → medium → hard)
- **Incorrect Answer**: Mastery adjusts, difficulty may decrease (hard → medium → easy)
- **Worked Examples**: Click "Show Example" for step-by-step solutions
- **Visual Progress**: Watch your mastery bar fill as you learn

## 📁 Project Structure

```
COM7032M_Final/
├── geotutor_main.py          # Main ITS application
├── generate_owl.py            # Original ontology generator
├── new_generate_owl.py        # Extended ontology generator (with Student/Resource)
├── GeoTutor.owl              # OWL ontology file (generated)
├── students_data.json         # Student profiles database (auto-created)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore                # Git ignore rules
```

## 🏗️ Architecture

### ITS Components

1. **Student Model**: BKT-based mastery tracking per student
2. **Expert Model**: OWL ontology with SWRL rules for area calculations
3. **Tutoring Model**: Adaptive difficulty adjustment and feedback generation
4. **Interface Model**: Tkinter GUI with matplotlib visualizations

### Ontology Structure

- **Classes**: `Shape`, `Triangle`, `Square`, `Rectangle`, `Student`, `Resource`
- **Data Properties**: `hasBase`, `hasHeight`, `hasSide`, `hasLength`, `hasWidth`, `hasArea`, `explains`, `hasMastery`, `hasDifficultyLevel`
- **Object Properties**: `studies` (Student → Resource), `requiresPrerequisite` (Resource → Resource)
- **SWRL Rules**: Automatic area calculation for each shape type

## 🔧 Configuration

### Student Data

Student profiles are stored in `students_data.json`:
```json
{
  "202300123": {
    "mastery": 0.75,
    "difficulty": "medium",
    "attempts": 15,
    "correct": 12,
    "last_login": "2025-12-02T15:30:00"
  }
}
```

### Ontology Customization

Edit `new_generate_owl.py` to:
- Add new shape types
- Modify SWRL rules
- Add new properties or relationships
- Create additional demo individuals

## 📊 Viewing the Ontology in Protégé

1. **Install Protégé**: Download from https://protege.stanford.edu/
2. **Open Ontology**: File → Open → Select `GeoTutor.owl`
3. **View Classes**: Entities → Classes tab
4. **View Properties**: Entities → Object properties / Data properties
5. **View Graph**: Window → Tabs → OntoGraf → Add classes and properties to see visual relationships

## 🐛 Troubleshooting

### "GeoTutor.owl not found"
- Run `python generate_owl.py` or `python new_generate_owl.py` first

### "Java not found" / Reasoner errors
- The app works without Java; ontology reasoning is optional
- If you want full reasoning, install Java JDK and ensure it's in your PATH

### "FileNotFoundError" when running
- Make sure you're in the project directory
- Check that `GeoTutor.owl` exists in the same folder

### Ontology won't open in Protégé
- Ensure the file is valid XML (first line should be `<?xml version="1.0"?>`)
- Regenerate using `new_generate_owl.py` if corrupted

## 📝 License

This project is for educational purposes (COM7032M Final Project).

## 👤 Author

Created for York St John University - COM7032M Final Project

## 🙏 Acknowledgments

- **owlready2**: Python library for OWL ontologies
- **Protégé**: Ontology editor and visualization
- **Tkinter & Matplotlib**: GUI and visualization libraries

---

**Note**: This ITS demonstrates full implementation of the four-model ITS architecture with ontology-based knowledge representation and adaptive learning algorithms.

