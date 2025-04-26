import os
from transformers import pipeline

# Disable oneDNN optimizations for potentially lower memory usage in TensorFlow
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load a smaller model for zero-shot classification
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-6")

# Define the text and candidate labels
text = "JB - SG CIQ egate 15 ppl Manual 5 ppl"
candidate_labels = ["customs traffic", "human traffic", "weather", "general info"]

# Perform zero-shot classification
results = classifier(text, candidate_labels)

# Print the results
print(results)
