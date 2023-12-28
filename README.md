# Vietnamese poem classification and evaluation 📜🔍

A Vietnamese poem classifer using [BertForSequenceClassification](https://huggingface.co/trituenhantaoio/bert-base-vietnamese-uncased) with the accuracy of ```99.7%```

This is a side project during the making of our [Vietnamese poem generator](https://github.com/Anshler/poem_generator)

## Features

* Classify Vietnamese poem into categories of ```4 chu```, ```5 chu```, ```7 chu```, ```luc bat``` and ```8 chu```
* Score the quality of each poem, based soldly on its conformation to the rigid rule of various types of Vietnamese poem. Using 3 criterias: Length, Tone and Rhyme as follow: ```score = L/10 + 3T/10 + 6R/10```

The rules for each genre are defined below:

| Genre | Length | Tone | Rhyme |
|------------------|------------------|--------------|------------------------|
| 4 chu    | - 4 words per line <br>- 4 lines per stanza (optional) | For each line: <br>- If the 2nd word is uneven (trắc), the 4th word is even (bằng) <br>- Vice versa | Last word (4th) of each line: <br>- Continuous rhyme (gieo vần tiếp) <br>- Alternating rhyme (gieo vần tréo) <br>- Three-line rhyme (gieo vần ba)|
| 5 chu    | - 5 words per line <br>- 4 lines per stanza (optional)  | Same as "4 chu" | Same as "4 chu" |
| 7 chu    | - 7 words per line <br>- 4 lines per stanza (optional) | For each line: <br>- If the 2nd word is uneven (trắc), the 4th word is even (bằng), the 6th word is uneven (trắc) <br> - 5th word and last word (7th) must have different tone | The last word of 1st, 2nd, 4th line per stanza must have same tone and rhyme |
| luc bat    | - 6 words in odd line <br>- 8 words in even line <br>- 4 lines per stanza (optional) | For 6-word line: <br>- If the 2nd word is uneven (trắc) the 4th word is even (bằng), the 6th word is uneven (trắc) <br><br> For 8-word line: <br>- Must be same as previous 6-word line <br>- The last word (8th) mut have same tone as 6th word | The last word (6th) in 6-word line must rhyme with the 6th word in the next 8-word line and the 8th word in the previous 8-word line |
| 8 chu    | - 8 words per line <br>- 4 lines per stanza (optional) | For each line: <br>- If the 3rd word is uneven (trắc), the 5th word is even (bằng), the 8th word is uneven (trắc)| Same as "4 chu" |




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
