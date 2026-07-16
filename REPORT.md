# Technical Report — Wasko Offline Health AI

**Team ID:** wasko_offline_health_ai  
**Domain:** Healthcare_Medical  
**Model:** TinyLlama-1.1B-Chat-v1.0

---

## Problem

<!-- Many communities across Africa have limited access to reliable healthcare information due to poor internet connectivity, shortages of healthcare professionals, language barriers, and limited access to digital medical resources. Most AI-powered health assistants depend on cloud services, making them unsuitable for rural clinics and remote communities where internet access is unreliable or unavailable. -->

Wasko Offline Health AI addresses this challenge by providing an entirely offline medical assistantcapable of answering health-related questions without requiring an internet connection. The application is designed for community health workers, students, rural clinics, and the general public.

The system currently supports both **English** and **Hausa**, enabling wider accessibility for users across Africa and other Hausa-speaking communities.

The solution focuses on delivering reliable medical education rather than replacing healthcare professionals. Users receive evidence-based health information retrieved from a curated offline medical knowledge base.

---

## Design Decisions

<!-- I selected **TinyLlama-1.1B-Chat-v1.0** because it provides an excellent balance between language quality, inference speed, and low hardware requirements.

The model is sufficiently small to execute efficiently on consumer laptops with approximately 8 GB RAM while still producing useful conversational responses.-->

- **Base model:** TinyLlama-1.1B-Chat-v1.0
- **Quantization:** GGUF Q4_K_M chosen because it provides an effective balance between inference quality, memory usage, and generation speed.
- **Alternatives considered:** Several model and quantization options were evaluated before selecting the final deployment configuration. - **GGUF Q8_0**. Produced slightly higher-quality responses but required significantly more memory, making it less suitable for deployment on the ADTC target hardware (8 GB RAM laptops). The increased memory footprint reduced the margin for running the application alongside the operating system and RAG pipeline. Final Choice: TinyLlama-1.1B-Chat-v1.0 (GGUF Q4_K_M)** – Selected because it provides the best balance of response quality, inference speed, and low memory consumption. During benchmarking, it achieved **12.37 tokens/second** while using approximately **1.15 GB Peak RAM**, enabling reliable offline deployment with Retrieval-Augmented Generation (RAG) on the ADTC reference laptop.

---

**Constraints

<!-- The design of Wasko Offline Health AI was driven by the hardware and infrastructure constraints common across many African communities, where reliable internet access and high-performance computing resources are often unavailable. -->

**Hardware Constraints

- **Target Platform:** Standard consumer laptop with **8 GB RAM**
- **CPU:** Intel64 Family 6 Model 61 (4-core equivalent)
- **GPU:** None (integrated graphics only)
- **Operating System:** Windows 10 (fully compatible with Ubuntu 22.04 via llama.cpp)
- **Inference Engine:** llama.cpp using GGUF models
- **Memory Budget:** Peak RSS of approximately **1.15 GB**, well within the ADTC hardware limit.

**Compute Constraints

- No GPU acceleration available.
- All inference is performed on the CPU using **llama.cpp**.
- The selected **TinyLlama-1.1B-Chat-v1.0 (GGUF Q4_K_M)** model provides a balance between response quality, memory efficiency, and inference speed on CPU-only hardware.

**Connectivity Constraints

- The application is designed to operate with **zero internet connectivity** during inference.
- No cloud APIs, remote databases, or external AI services are required after installation.
- All model weights, medical documents, and retrieval indexes are stored locally.

**Data Availability Constraints

- Medical responses are generated from a curated offline knowledge base covering common diseases and public health topics relevant to African communities.
- The system supports **English and Hausa**, improving accessibility for users with limited English proficiency.
- Knowledge updates require updating the local document repository rather than relying on online services.

**Deployment Constraints

The solution was designed to satisfy the Africa Deep Tech Challenge deployment requirements:

- Fully offline operation
- CPU-only inference via llama.cpp
- Compatible with 8 GB RAM laptops
- No external network calls during inference
- Portable binary bundle using GGUF model weights

---

## Benchmarks

<!-- The project was benchmarked using the official ADTC Profiler -->

| Metric | Result |
|---------|---------|
| Model | TinyLlama-1.1B-Chat-v1.0.Q4_K_M |
| Runtime | llama.cpp |
| Generation Throughput | 12.37 tokens/sec |
| First Token Latency | 14.44 seconds |
| Peak Memory (RSS) | 1173.1 MB |
| Steady Memory | 1119.62 MB |
| Peak Virtual Memory | 605.12 MB |
| CPU Utilization (P99) | 77.7% |
| Thermal Throttling | No |
| Context Length | 2048 tokens |

These are self-reported development benchmarks. Scores are measured by the ADTC profiler on the participant's laptop.

**ADTC Profiler Scores

| Score | Result |
|---------|---------|
| Self-Reported Performance (Sperf) | **82.47 / 100** |
| Self-Efficacy (Seff) | **83.63 / 100** |

These scores indicate that the system delivers strong performance while remaining within the resource constraints required by the challenge.
