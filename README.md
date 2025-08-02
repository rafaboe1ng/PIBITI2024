# PIBITI2024
Ontology + SWRL + Python engine to infer post-it assembly instructions.

## Features

- **Dynamic order modeling**  
  Create a new order individual in the ontology simply by entering a client name and choosing a Post-it color (Blue, Green, Pink or Yellow).

- **Automated reasoning**  
  Uses Pellet via Owlready2 to infer which assembly steps are required for each color.

- **Step sequencing**  
  Orders the inferred steps by their defined `sequence` property.

- **PDF export**  
  Generates a numbered PDF of the instructions using ReportLab/Platypus.

---

## Prerequisites

- **Python 3.7+**  
- **Java Runtime Environment** (required by Pellet)  
- **pip** packages:
  ```bash
  pip install -r requirements.txt