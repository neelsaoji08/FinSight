import pandas as pd
import numpy as np
from tqdm import tqdm 
from transformers import AutoTokenizer,DataCollatorWithPadding,AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
import evaluate
import torch
from peft import PeftModel, PeftConfig, get_peft_model, LoraConfig
from sklearn.metrics import classification_report  


id2label = {0: "positive", 1: "neutral", 2: "negative"}
label2id = {"positive": 0, "neutral": 1, "negative": 2}



class BertDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels, label2id):
        self.encodings = encodings
        self.labels = [label2id[value] for value in labels]

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]).to('cuda:0') for key, val in self.encodings.items()}
        # Move labels tensor to 'cuda:0'
        item['labels'] = torch.tensor(self.labels[idx]).to('cuda:0')
        return item

    def __len__(self):
        return len(self.labels)

def compute_metrics(eval_pred):
    accuracy= evaluate.load('accuracy')
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)



def model_train(model,tokenizer,path,name):
    data=pd.read_csv(path,encoding='latin-1', header=None)
    data.columns=['labels','text']

    
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    texts = data["text"].to_list()
    labels = data["labels"].to_list()
    text_train, text_test, labels_train, labels_test = train_test_split(  
        texts, labels, test_size=0.20, random_state=42,   
    )  
    tokenized_text_train = tokenizer(text_train,truncation=True)
    tokenized_text_test = tokenizer(text_test,truncation=True)

    print("train size:", len(labels_train))
    print("test size:", len(labels_test))



    train_dataset = BertDataset(tokenized_text_train, labels_train, label2id)
    test_dataset = BertDataset(tokenized_text_test, labels_test, label2id)
    
    if name=='distilbert':
        peft_config = LoraConfig(task_type="SEQ_CLS",
                        r=8,
                        lora_alpha=32,
                        lora_dropout=0.01,
                        target_modules = ['q_lin']
                            )
    else:
         peft_config = LoraConfig(task_type="SEQ_CLS",
                        r=8,
                        lora_alpha=32,
                        lora_dropout=0.01
                            )
        

    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    training_args = TrainingArguments(
    output_dir=f"new_model_{name}",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=15,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    push_to_hub=False,
    report_to="none"
    )

    trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    )
    trainer.train()
    model = trainer.model
    
    
    return model,text_train,text_test,labels_train,labels_test,labels

