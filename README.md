# Sentiment_Analysis
Sentiment Analysis using the DistilBERT Model from Huggingface.co for the introduction to data science course <br> <br>
Download Chromedriver from https://chromedriver.chromium.org

## Sentiment Model with a training dataset size of 3000 entries and test dataset of 300 entries:
https://huggingface.co/mwinterhalter/finetuning-sentiment-model-3000-samples <br>
Loss: 0.3119 <br>
Accuracy: 0.8833 <br>
F1: 0.8845 <br>

## Sentiment Model with a training dataset size of 25000 entries and test dataset of 12500 entries and increased epochs:
https://huggingface.co/mwinterhalter/my-sentiment-model <br>
Loss: 0.3033 <br>
Accuracy: 0.9301 <br>
F1: 0.9302 <br>

New eval metrics using 25k test data entries and 4 epochs: <br>
Loss: 0.3230 <br>
Accuracy: 0.9307 <br>
F1: 0.9315 <br>

Slighlty higher loss but accuracy slightly increased. <br>
Trying to increase the batch size next.
