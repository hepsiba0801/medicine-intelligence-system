# Medicine Intelligence System

## AI-Powered Medicine Validation, Classification and Inventory Intelligence Platform

---

# Overview

Medicine Intelligence System is a Data Science and Applied Artificial Intelligence project designed to improve the quality, consistency, and reliability of medicine inventory data.

The system automatically validates medicine names, detects invalid entries, corrects spelling mistakes, classifies medicines into therapeutic categories, and maintains a clean medicine knowledge base using Large Language Models (LLMs).

Unlike traditional inventory systems that reject invalid inputs, this project follows a non-blocking validation architecture, ensuring that all user data is preserved while intelligent validation and classification are performed in the background.

---

# Project Type

### Domain

Healthcare Analytics

### Category

Data Science Project

### Focus Areas

* Data Validation
* Data Quality Engineering
* NLP
* Large Language Models (LLMs)
* Classification Systems
* Knowledge Base Construction
* AI Evaluation and Benchmarking

---

# Problem Statement

Medicine inventory systems frequently suffer from:

* Misspelled medicine names
* Duplicate entries
* Invalid products
* Inconsistent categorization
* Manual verification effort
* Poor data quality

These issues reduce inventory reliability and increase operational overhead.

The objective of this project is to create an intelligent validation and classification pipeline capable of automatically processing medicine records and maintaining a clean, structured inventory.

---

# Project Objectives

* Validate medicine names
* Detect non-medicine entries
* Correct spelling mistakes
* Categorize medicines automatically
* Maintain a centralized medicine knowledge base
* Support bulk inventory uploads
* Benchmark multiple LLMs
* Measure model reliability using evaluation metrics

---

# Design Philosophy

## Non-Blocking Data Ingestion

A major architectural decision in this project was to avoid blocking user input.

Most validation systems follow:

```text
User Input
    ↓
Validation
    ↓
Accept / Reject
```

Rejected records are often lost permanently.

Instead, this project follows:

```text
User Input
    ↓
Medicine Inventory
(Raw Data Storage)
    ↓
Validation Engine
    ↓
Classification Engine
    ↓
Clean Inventory
```

### Why?

Real-world inventory systems contain:

* Typographical errors
* New medicines
* Human mistakes
* Incomplete records

Blocking data at ingestion can lead to information loss.

### Benefits

* No loss of user-submitted data
* Complete audit trail
* Better model retraining opportunities
* Human review support
* Enterprise-ready architecture

---

# System Architecture

```text
User Input
     │
     ▼
Medicine Inventory
(Raw Records)
     │
     ▼
Validation Engine
     │
 ┌───────────────┐
 │               │
 ▼               ▼
Valid          Invalid
Records        Records
 │
 ▼
Classification Engine
 │
 ▼
Clean Inventory
 │
 ▼
Medicine Master
(Knowledge Base)
```

---

# Technology Stack

## Programming Language

* Python

## Backend

* FastAPI

## Database

* MySQL
* SQLAlchemy ORM

## Machine Learning & AI

* GPT-OSS
* Llama 3.2
* Qwen

## Evaluation

* Scikit-Learn
* Accuracy Score
* F1 Score

---

# Database Design

## Medicine Inventory

Stores raw user submissions.

### Fields

* id
* medicine_name
* stock_quantity

Purpose:

* Preserve original user input
* Maintain audit history

---

## Clean Inventory

Stores validated medicine records.

### Fields

* id
* source_id
* medicine_name
* suggested_name
* stock_quantity
* is_medicine
* classification
* classification_confidence
* reason

Purpose:

* Structured and validated inventory

---

## Medicine Master

Central medicine knowledge repository.

### Fields

* id
* medicine_name
* category
* confidence

Purpose:

* Prevent duplicate classification
* Build reusable medicine knowledge

---

## Cache Inventory

Temporary storage for bulk uploads.

### Fields

* id
* medicine_name
* stock_quantity

Purpose:

* Batch processing
* Improved scalability

---

# Project Evolution

---

# Phase 1 — Medicine Validation

### Goal

Determine whether an inventory item is a medicine.

### Features

* Medicine detection
* Non-medicine detection
* Input validation

### Example

Input:

```text
Paracetamol
```

Output:

```json
{
  "is_medicine": true
}
```

---

Input:

```text
Laptop
```

Output:

```json
{
  "is_medicine": false,
  "reason": "Electronic device"
}
```

---

# Phase 2 — LLM-Based Medicine Classification

### Goal

Automatically classify medicines into therapeutic categories.

### Categories

* Antibiotic
* Antiviral
* Antifungal
* Analgesic
* Antidiabetic
* Antihypertensive
* Antacid
* Vitamin
* Supplement
* Cardiovascular
* Respiratory
* Antidepressant
* Antipsychotic
* Corticosteroid

### Example

Input:

```text
Paracetamol
```

Output:

```json
{
  "category": "Analgesic"
}
```

---

# Phase 3 — Bulk Processing Architecture

### Goal

Support large-scale inventory ingestion.

### Single Record Flow

```text
User Input
     ↓
Validation
     ↓
Clean Inventory
```

### Bulk Flow

```text
CSV Upload
     ↓
Cache Inventory
     ↓
Validation Engine
     ↓
Classification Engine
     ↓
Clean Inventory
     ↓
Medicine Master
```

### Benefits

* Faster processing
* Better scalability
* Reduced API latency
* Enterprise-ready workflow

---

# Phase 4 — Medicine Knowledge Base

### Goal

Create a reusable medicine repository.

### Features

* Unique medicine storage
* Duplicate prevention
* Category persistence
* Confidence tracking

### Example

```text
Paracetamol
Category: Analgesic
```

Stored once and reused.

---

# Phase 5 — Multi-LLM Evaluation Framework

### Goal

Evaluate and compare multiple Large Language Models.

### Models Evaluated

* GPT-OSS
* Llama 3.2
* Qwen

### Metrics

* Accuracy
* F1 Score
* Latency
* Consensus Agreement

---

# Evaluation Methodology

A curated medicine benchmark dataset was created to evaluate model performance.

### Accuracy

Measures the percentage of correctly classified medicines.

### F1 Score

Measures the balance between precision and recall.

### Latency

Measures average response time.

### Consensus

Measures agreement between multiple models.

---

# Benchmark Results

| Model     | Accuracy | F1 Score | Avg Latency |
| --------- | -------- | -------- | ----------- |
| GPT-OSS   | 1.0000   | 1.0000   | 2.91 sec    |
| Qwen      | 1.0000   | 1.0000   | 225.74 sec  |
| Llama 3.2 | 0.9600   | 0.9596   | 36.99 sec   |

---

# Key Data Science Concepts Demonstrated

* Data Validation
* Data Quality Engineering
* NLP Classification
* LLM-Based Classification
* Knowledge Base Construction
* AI Model Evaluation
* Accuracy Analysis
* F1 Score Analysis
* Consensus-Based AI Systems
* Benchmarking Frameworks

---

# Future Enhancements

## Phase 6

Consensus Classification Engine

```text
GPT-OSS
   │
Llama
   │
Qwen
   │
Consensus Decision
```

---

## Phase 7

Human-in-the-Loop Validation

```text
Unknown Medicine
       ↓
Human Review
       ↓
Knowledge Base Update
```

---

## Phase 8

Domain-Aware Medical Assistant

Specialized medicine intelligence chatbot with fallback LLM routing.

---

# Conclusion

Medicine Intelligence System demonstrates how Data Science, NLP, and Large Language Models can be combined to improve medicine inventory quality through automated validation, classification, and knowledge base construction.

The project evolved from a simple validation engine into a scalable AI-powered inventory intelligence platform featuring multi-LLM benchmarking, bulk processing pipelines, and enterprise-oriented data quality workflows.

---

# Author

**Hepsiba Preetha**

B.Tech Artificial Intelligence and Data Science

