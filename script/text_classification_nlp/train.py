from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import DataCollatorForTokenClassification
from transformers import BertConfig
from transformers import BertModel,AutoModel
import os
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
import numpy as np
from datasets import load_metric
import wandb
os.environ["WANDB_API_KEY"]="482af50437ce97c6a61cebe16c67ef3416b79bbf"
os.environ["WANDB_ENTITY"]="huhao"
os.environ["WANDB_PROJECT"]="nlp_text_classification"
dataset = load_dataset("wikiann", "bn")
label_names = dataset["train"].features["ner_tags"].feature.names
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
# Get the values for input_ids, token_type_ids, attention_mask
def tokenize_adjust_labels(all_samples_per_split):
    tokenized_samples = tokenizer.batch_encode_plus(all_samples_per_split["tokens"], is_split_into_words=True)
    # tokenized_samples is not a datasets object so this alone won't work with Trainer API, hence map is used
    # so the new keys [input_ids, labels (after adjustment)]
    # can be added to the datasets dict for each train test validation split
    total_adjusted_labels = []
    print(len(tokenized_samples["input_ids"]))
    for k in range(0, tokenized_samples["input_ids"]):
        prev_wid = -1
        word_ids_list = tokenized_samples.word_ids(batch_index=k)
        existing_label_ids = all_samples_per_split["ner_tags"][k]
        i = -1
        adjusted_label_ids = []

        for wid in word_ids_list:
            if (wid is None):
                adjusted_label_ids.append(-100)
            elif (wid != prev_wid):
                i = i + 1
                adjusted_label_ids.append(existing_label_ids[i])
                prev_wid = wid
            else:
                label_name = label_names[existing_label_ids[i]]
                adjusted_label_ids.append(existing_label_ids[i])

        total_adjusted_labels.append(adjusted_label_ids)
    tokenized_samples["labels"] = total_adjusted_labels
    return tokenized_samples
tokenized_dataset = dataset.map(tokenize_adjust_labels, batched=True)
data_collator = DataCollatorForTokenClassification(tokenizer)
metric = load_metric("seqeval")
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)
    # Remove ignored index (special tokens)
    true_predictions = [
        [label_names[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_names[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    results = metric.compute(predictions=true_predictions, references=true_labels)
    flattened_results = {
        "overall_precision": results["overall_precision"],
        "overall_recall": results["overall_recall"],
        "overall_f1": results["overall_f1"],
        "overall_accuracy": results["overall_accuracy"],
    }
    for k in results.keys():
      if(k not in flattened_results.keys()):
        flattened_results[k+"_f1"]=results[k]["f1"]

    return flattened_results
model = AutoModelForTokenClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(label_names))
# config = AutoModelForTokenClassification.from_pretrained('bert-base-multilingual-cased',num_labels=len(label_names))    # Download configuration from S3 and cache.
# model = AutoModel.from_config(config)  # E.g. model was saved using `save_pretrained('./test/saved_model/')`
training_args = TrainingArguments(
    output_dir="./fine_tune_bert_output",
    evaluation_strategy="steps",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=7,
    weight_decay=0.01,
    logging_steps = 1000,
    report_to="wandb",
    run_name = "ep_10_tokenized_11",
    save_strategy='no'
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

wandb.finish()