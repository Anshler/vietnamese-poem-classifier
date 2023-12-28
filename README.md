# Vietnamese poem classifier and evaluator 📜🔍

A Vietnamese poem classifer using [BertForSequenceClassification](https://huggingface.co/trituenhantaoio/bert-base-vietnamese-uncased) with the accuracy of ```99.7%```

This is a side project during the making of our [Vietnamese poem generator](https://github.com/Anshler/poem_generator)

## Features

* Classify Vietnamese poem into categories of ```4 chu```, ```5 chu```, ```7 chu```, ```luc bat``` and ```8 chu```
* Score the quality of each poem, based soldly on its conformation to the rigid rule of various types of Vietnamese poem. Using 3 criterias: Length, Tone and Rhyme as follow: ```score = L/10 + 3T/10 + 6R/10```

The rule for each genre is as followed:

| Genre | Rule |
|------------------|------------------|
| 4 chu    | - Length: 4 words per line, 4 lines per stanza (optional) <br>- Tone: for each line, if the 2nd word is uneven (trắc), the 4th word is even (bằng), and vice versa <br>- Rhyme: divided into continuous rhyme (gieo vần tiếp), alternating rhyme (gieo vần tréo) and three-line rhyme (gieo vần ba) for the last word of each line|
| 5 chu    | - Length: 5 words per line, 4 lines per stanza (optional)  <br>- Tone and Rhyme: same as "4 chu" |
| 7 chu    | - Length: 7 words per line, 4 lines per stanza (optional) <br>- Tone: for each line, if the 2nd word is uneven (trắc), the 4th word is even (bằng), the 6th word is uneven (trắc), and vice versa <br>- 5th word and last word (7th) must have different tone <br>- Rhyme: the last word of 1st, 2nd, 4th line per stanza must have same tone and rhyme |
| luc bat    | - Length: 6 words in odd line, 8 words in even line, 4 lines per stanza (optional) <br>- Tone: for 6-word line, if the 2nd word is uneven (trắc) the 4th word is even (bằng), the 6th word is uneven (trắc), the following 8-word line must be the same, the last word (8th) mut have same tone as 6th word <br>- Rhyme: the last word (6th) in 6-word line must rhyme with the 6th word in the next 8-word line, as well as the 8th word in the previous 8-word line |
| 8 chu    | - Length: 8 words per line, 4 lines per stanza (optional)    |




## Data

A colelction of 171188 Vietnamese poems with different genres: luc-bat, 5-chu, 7-chu, 8-chu, 4-chu. Download [here](https://github.com/fsoft-ailab/Poem-Generator/raw/master/dataset/poems_dataset.zip)

For more detail, refer to the _Acknowledgments_ section

## Training

Training code is in our repo [Vietnamese poem generator](https://github.com/Anshler/poem_generator)

Run:
```
python poem_classifier_training.py
```

## Installation

```
pip install vietnamese-poem-classifier
```
Or

```
pip install git+https://github.com/Anshler/vietnamese-poem-classifier
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

#>> [{'label': 'luc bat', 'confidence': 0.9999017715454102, 'poem_score': 0.75}]
```

## Model

The model's weights are published at Huggingface [Anshler/vietnamese-poem-classifier](https://huggingface.co/Anshler/vietnamese-poem-classifier) 

## Acknowledgments

_This project was inspired by the evaluation method from ```fsoft-ailab```_'s_ [SP-GPT2 Poem-Generator](https://github.com/fsoft-ailab/Poem-Generator)

_Dataset also taken from their repo_
