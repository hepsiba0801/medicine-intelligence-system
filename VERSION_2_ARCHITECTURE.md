# Version 2 - LLM Validation Pipeline

## Architecture

User Input
    ↓
MedicineInventory
    ↓
POST /inventory/clean
    ↓
GPT-OSS Validation
    ↓
Spell Correction
    ↓
Category Classification
    ↓
CleanInventory

## Features

- Raw inventory preserved
- LLM medicine validation
- LLM spelling correction
- LLM category classification
- Non-medicines filtered out
- Clean inventory generation

## Tables

### medicine_inventory

- id
- medicine_name
- quantity

### clean_inventory

- id
- source_id
- medicine_name
- suggested_name
- stock_quantity
- classification
- classification_confidence