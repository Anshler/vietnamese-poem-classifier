# Vietnamese poem classifier and evaluator 📜🔍

A Vietnamese poem classifer using [BertForSequenceClassification](https://huggingface.co/trituenhantaoio/bert-base-vietnamese-uncased) with the accuracy of ```99.7%```

This is a side project during the making of our [Vietnamese poem generator](https://github.com/Anshler/poem_generator)

## Features

* Classify Vietnamese poem into categories of ```4 chu```, ```5 chu```, ```7 chu```, ```luc bat``` and ```8 chu```
* Score the quality of each poem, based soldly on its conformation to the rigid rule of various types of Vietnamese poem. Using 3 criterias: Length, Tone and Rhyme as follow: ```score = L/10 + 3T/10 + 6R/10```

## Data

A colelction of 171188 Vietnamese poems with different genres: luc-bat, 5-chu, 7-chu, 8-chu, 4-chu. Download [here](https://github.com/fsoft-ailab/Poem-Generator/raw/master/dataset/poems_dataset.zip)

For more detail, refer to the _Acknowledgments_ section

## Training

Training code is in our repo [Vietnamese poem generator](https://github.com/Anshler/poem_generator)

Run:
```
python poem_classifier_training.py
```

## Inference

```python
from vietnamese_poem_classifier.poem_classifier import PoemClassifier

classifier = PoemClassifier()

poem = '''Người đi theo gió đuổi mây
          Tôi buồn nhặt nhạnh tháng ngày lãng quên
          Em theo hú bóng kim tiền
          Bần thần tôi ngẫm triền miên thói đời.'''

classifier.predict(poem)
```

```
>> [{'label': 'luc bat', 'confidence': 0.9999017715454102, 'poem_score': 0.75}]
```
## Model

The weights of our model can be downloaded from Huggingface at [Anshler/vietnamese-poem-classifier](https://huggingface.co/Anshler/vietnamese-poem-classifier) 

## Acknowledgments

_This project was inspired by the evaluation method from ```fsoft-ailab```_'s_ [SP-GPT2 Poem-Generator](https://github.com/fsoft-ailab/Poem-Generator)

_Dataset also taken from their repo_
