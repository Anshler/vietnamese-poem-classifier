import pandas as pd
import ast
import re
from transformers import pipeline
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

def load_data(filename: str):
    with resources.open_text("vietnamese_poem_classifier", filename) as file:
        text = file.read()
    content = ast.literal_eval(text)
    return content

vowels_path = "start_vowels.txt"
start_vowels = load_data(vowels_path)

huyen = start_vowels['huyen']
sac = start_vowels['sac']
nang = start_vowels['nang']
hoi = start_vowels['hoi']
nga = start_vowels['nga']
khong_dau = start_vowels['khong_dau']

list_start_vowels = []
list_start_vowels.extend(huyen)
list_start_vowels.extend(sac)
list_start_vowels.extend(nang)
list_start_vowels.extend(hoi)
list_start_vowels.extend(nga)
list_start_vowels.extend(khong_dau)

rhyme_path = "rhymes.txt"
rhymes_dict = load_data(rhyme_path)

uneven_chars = []
uneven_chars.extend(sac)
uneven_chars.extend(hoi)
uneven_chars.extend(nga)
uneven_chars.extend(nang)

def is_stanza(sentences: str):
    """
      Check if input is a stanza or not
      param sentences: sentences to check
      return: is stanza or not
    """
    return len(sentences.split("\n\n")) == 1


def split_word(word):
    """
        Split word by 2 part, starting and ending
        param word: word to split
        return: ending part of word
        Ex: mùa -> ùa
    """
    word_length = len(word)
    start_index = 0
    prev = ''
    for i in range(word_length):
        if prev == 'g' and word[i] == 'i':
            continue
        if prev == 'q' and word[i] == 'u':
            continue
        if word[i] in list_start_vowels:
            start_index = i
            break
        prev = word[i]
    return word[start_index:]


def compare(word1: str, word2: str):
    """
      Check 2 words rhyme if the same
      param word1, word2: words to check
      return: is the same rhyme or not
    """
    rhyme1 = split_word(word1)
    rhyme2 = split_word(word2)

    if rhyme2 in rhymes_dict[rhyme1]:
        return True
    return False

def stanza_rhyme_score(word_list):
    """
        param: word_list (list of words in a stanza to be checked)
        return: list of rhyme groups
    """
    rhyme_groups = []
    visited = set()
    for i, word1 in enumerate(word_list):
        if i in visited:
            continue
        rhymes_with_word1 = [word1]
        for j, word2 in enumerate(word_list[i+1:]):
            if compare(word1, word2):
                rhymes_with_word1.append(word2)
                visited.add(j+i+1)
        rhyme_groups.append(rhymes_with_word1)
    return sorted([len(x) for x in rhyme_groups], reverse=True)

def stanza_rhyme_score_457(word_list, line_count):
    score_1 = stanza_rhyme_score(word_list)
    if len(word_list) ==4 or (line_count==3 and len(word_list)==3):
        word_list.remove(word_list[-2])
        score_2 = stanza_rhyme_score(word_list)
        if score_2[0]!= len(word_list) and score_1[0]==len(word_list):
            score_1[0] = score_1[0]-0.4
    return score_1

def stanza_rhyme_score_8(rhyme_group):
    rhyme_score_continuous = 0
    rhyme_score_continuous_shifted = 0
    rhyme_score_alternate = 0
    rhyme_score_surround = 0
    line_count = len(rhyme_group)
    for i in range(0, line_count,4):
        # Continuous
        try:
            if compare(rhyme_group[i],rhyme_group[i+1]):
                rhyme_score_continuous +=2/line_count
        except: pass
        try:
            if compare(rhyme_group[i+2],rhyme_group[i+3]):
                rhyme_score_continuous +=2/line_count
        except: pass

        # Alternate
        try:
            if compare(rhyme_group[i],rhyme_group[i+2]):
                rhyme_score_alternate +=2/line_count
        except: pass
        try:
            if compare(rhyme_group[i+1],rhyme_group[i+3]):
                rhyme_score_alternate +=2/line_count
        except: pass

        # Surround
        try:
            if compare(rhyme_group[i],rhyme_group[i+3]):
                rhyme_score_surround +=2/line_count
        except: pass
        try:
            if compare(rhyme_group[i+1],rhyme_group[i+2]):
                rhyme_score_surround +=2/line_count
        except: pass

    #print(line_count)
    line_count-=1
    if line_count%2 != 0:
        line_count-=1
    #print(line_count)

    for i in range(1, len(rhyme_group), 4):
        # Surround
        try:
            if compare(rhyme_group[i],rhyme_group[i+1]):
                rhyme_score_continuous_shifted +=2/line_count
        except: pass
        try:
            if compare(rhyme_group[i+2],rhyme_group[i+3]):
                rhyme_score_continuous_shifted +=2/line_count
        except: pass
    return max(rhyme_score_surround, rhyme_score_alternate, rhyme_score_continuous, rhyme_score_continuous_shifted)

def get_tone(word: str, chars = uneven_chars):
    """
        Check word is even tone or not
        param word: word to check tone
        return: even or uneven
    """
    # Thay uneven_chars bằng huyen để phân biệt ko_dau và huyen
    vowel = split_word(word)
    first_char = vowel[0]
    if first_char in chars:
        return 'uneven'
    try:
        second_char = vowel[1]
        if second_char in chars:
            return 'uneven'
    except:
        pass
    return 'even'

def stanza_tone_score_45(tone_group):
    # Mỗi hàng chỉ cần chữ 2nd và 4th khác tone là có điểm
    tone_score = 0
    for x, y in zip(tone_group[::2], tone_group[1::2]):
        try:
            if get_tone(x) != get_tone(y):
                tone_score+=1
        except: pass
    return tone_score

def stanza_tone_score_68(tone_group_6, tone_group_8):
    # Hàng 6 luật 2-4-6 là B-T-B
    # Hàng 8 luật 2-4-6-8 là B-T-B-B, chữ 6th và 8th khác dấu
    tone_score = 0
    for x, y, z in zip(*[iter(tone_group_6)]*3):
        try:
            if get_tone(x) == 'even':
                tone_score += 1/3
            if get_tone(y) == 'uneven':
                tone_score += 1/3
            if get_tone(z) == 'even':
                tone_score += 1/3
        except:
            pass
        #print(tone_score)
    for x, y, z, t in zip(*[iter(tone_group_8)]*4):
        try:
            if get_tone(x) == 'even':
                tone_score += 1/5
            if get_tone(y) == 'uneven':
                tone_score += 1/5
            if get_tone(z) == 'even':
                tone_score += 1/5
            if get_tone(t) == 'even':
                tone_score += 1/5
            if get_tone(z,huyen) != get_tone(t,huyen): # Hai âm bằng 6th, 8th phải khác dấu
                tone_score += 1/5
        except:
            pass
        #print(tone_score)
    return round(tone_score,4)

# -----------------------------------------TONE SCORE 7 CHU-------------------------------------------
def stanza_endtone_score(rhyming_tone_group):
    """
        param: word_list (list of words in a stanza to be checked)
        return: list of rhyme groups
    """
    tone_group = []
    visited = set()
    for i, word1 in enumerate(rhyming_tone_group):
        if i in visited:
            continue
        rhymes_with_word1 = [word1]
        for j, word2 in enumerate(rhyming_tone_group[i+1:]):
            if get_tone(word1) == get_tone(word2):
                rhymes_with_word1.append(word2)
                visited.add(j+i+1)
        tone_group.append(rhymes_with_word1)
    return sorted([len(x) for x in tone_group], reverse=True)[0]

def bang_trac(tone_group, rule: str): # Thay vì viết 2 lần, tạo hàm riêng để xài chung
    tone_score = 0
    for i in range(len(tone_group)):
        try:
            if i in [0,2,5,9,12,14] and get_tone(tone_group[i]) == rule:
                #print(tone_group[i])
                tone_score += 1/4
            if i in [1,4,6,8,10,13] and get_tone(tone_group[i]) != rule:
                tone_score += 1/4
        except: pass
    return tone_score

def stanza_tone_score_7(tone_group, rule = ''):
    '''
    Luật vần bằng: x là chữ thứ 7th, so tone riêng với nhau
        B-T-B-x
        T-B-T-x
        T-B-T-x
        B-T-B-x
    Luật vần trắc:
        Ngược lại
    '''
    score = 0
    #print(tone_group)
    if rule == '':
        score_1 = bang_trac(tone_group, 'even') # xem luật bằng hay luật trắc cho điểm cao hơn, cái nào cao hơn theo cái đó
        score_2 = bang_trac(tone_group, 'uneven')
        if score_1>=score_2:
            rule = 'even'
            score = score_1
        else:
            rule = 'uneven'
            score = score_2
    else:
        score = bang_trac(tone_group,rule)

    # -------------Rhyming Tone Score-----------------
    rhyming_tone_group = []
    for i in range(len(tone_group)): # append every 7th words
        if i in [3,7,11,15]:
            #print(tone_group[i])
            rhyming_tone_group.append(tone_group[i])

    end_count = len(rhyming_tone_group)
    if end_count <=1:
        return round(score, 4), rule
    if end_count == 2:
        try:
            if get_tone(rhyming_tone_group[0]) == get_tone(rhyming_tone_group[1]):
                return round((score + end_count/4), 4), rule
        except: pass
        return round(score, 4), rule

    # Nếu > 3 hàng thì hàng 2 dưới đếm lên chữ 7th phải khác tone mấy chữ 7th hàng khác
    same_tone_group = rhyming_tone_group
    if end_count >=3:
        oppo_tone_group = same_tone_group[-2]
        same_tone_group.remove(same_tone_group[-2])

    while ("" in same_tone_group):
        same_tone_group.remove("")

    #print(same_tone_group)
    #print((oppo_tone_group))
    same_tone_score = 0
    oppo_tone_score = 0
    try:
        same_tone_score = stanza_endtone_score(same_tone_group)/(end_count-1)
    except: pass
    #print(same_tone_score)

    if oppo_tone_group == '':
        return round((score+same_tone_score/2),4), rule
    try:
        for x in same_tone_group:
            if get_tone(oppo_tone_group) != get_tone(x):
                oppo_tone_score+= 1/(end_count-1)
    except: pass
    #print(oppo_tone_score)

    return round((score+(same_tone_score + oppo_tone_score)/2),4), rule

# -----------------------------------------TONE SCORE 8 CHU-------------------------------------------
def tone_module(tone_groups,i, rule):
    even_score = 0
    uneven_score = 0
    if get_tone(tone_groups[i][0]) == rule: even_score += 1 / 3
    else: uneven_score += 1 / 3

    try:
        if get_tone(tone_groups[i][1]) != rule or get_tone(tone_groups[i][2]) != rule: even_score += 1 / 3
    except: pass
    try:
        if get_tone(tone_groups[i][1]) == rule or get_tone(tone_groups[i][2]) == rule: uneven_score += 1 / 3
    except: pass
    try:
        if get_tone(tone_groups[i][3]) == rule: even_score += 1 / 3
        else: uneven_score += 1 / 3
    except: pass
    return even_score, uneven_score

def tone_continuous(tone_groups):
    even_score = 0
    uneven_score = 0
    for i in range(0, len(tone_groups), 4):
        try:
            even_score_, uneven_score_ = tone_module(tone_groups,i,'even')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i+1, 'even')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i + 2, 'uneven')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i + 3, 'uneven')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass

    if even_score>= uneven_score:
        return even_score
    return uneven_score

def tone_alternate(tone_groups):
    even_score = 0
    uneven_score = 0
    for i in range(0, len(tone_groups), 4):
        try:
            even_score_, uneven_score_ = tone_module(tone_groups,i,'even')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i+1, 'uneven')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i + 2, 'even')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i + 3, 'uneven')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass

    if even_score>= uneven_score:
        return even_score
    return uneven_score

def tone_surround(tone_groups):
    even_score = 0
    uneven_score = 0
    for i in range(0, len(tone_groups), 4):
        try:
            even_score_, uneven_score_ = tone_module(tone_groups,i,'even')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i+1, 'uneven')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i + 2, 'uneven')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass
        try:
            even_score_, uneven_score_ = tone_module(tone_groups, i + 3, 'even')
            even_score += even_score_
            uneven_score += uneven_score_
        except: pass

    if even_score>= uneven_score:
        return even_score
    return uneven_score

def max_tone_score_8_chu(tone_groups):
    score_continuous = tone_continuous(tone_groups)
    score_alternate = tone_alternate(tone_groups)
    score_surround = tone_surround(tone_groups)
    return max(score_surround, score_alternate, score_continuous)

# --------------------------------------------------------------------------------------------
def stanza_len_score(lines, x: int,y: int):
    """
        lines: lines in the stanza (list)
        x: odd line word count
        y: even line word count -> (x=6 , y=8) -> luc bat
        lines count must be even (2 or 4), penalty if odd
    """
    score = 0
    for i in range(0,len(lines),2):
        if len(lines[i].split(' ')) == x:
                score+=1
        try:
            if len(lines[i+1].split(' ')) == y:
                score += 1
        except: pass

    return score

def preprocess_stanza(stanza: str):
    """
       A function to process Stanza to remove all unnecessary blank
       param sentence: stanza to process
       return: stanza processed
     """
    sentences = stanza.split("\n")
    sentences_out = []
    for sentence in sentences:
        words = sentence.split(" ")
        words_out = []
        for word in words:
            if word:
                words_out.append(word)
        sentences_out.append(" ".join(words_out))
    return "\n".join(sentences_out)

def preprocess_linebreaks(text: str):
    # Replace 3 or more linebreaks with double linebreaks
    if text[0] == '\n':
        text = text[1:]
    if text[-1]== '\n':
        text = text[:-1]
    text = text.replace('.','')
    return re.sub(r'(\n){3,}', '\n\n', text)

# ------------------------------------------4 CHU---------------------------------------------------
def check_rule_4_chu(stanza: str):
    lines = stanza.split('\n')
    if len(lines)%2 ==0:
        len_score = stanza_len_score(lines,4,4)/len(lines)
    else:
        len_score = stanza_len_score(lines,4,4)/(len(lines)+1)
    tone_score = 0
    rhyme_score = 0
    tone_group = []
    rhyme_group = []
    for line in lines:
        words = line.split(' ')
        # append every 2nd and 4th word to tone_group
        # append every 4th word to rhyme_group
        try:
            tone_group.append(words[1])
        except: tone_group.append('')
        try:
            tone_group.append(words[3])
            rhyme_group.append(words[3])
        except: tone_group.append('')
    try:
        tone_score = tone_score + stanza_tone_score_45(tone_group)/len(lines)
    except: pass

    try:
        if len(lines) == 1: rhyme_score = 0
        else:
            rhyme_score_list = stanza_rhyme_score_457(rhyme_group, len(lines))
            if rhyme_score_list[0]>=3 or (len(lines) == 4 and rhyme_score_list[0]==2 and rhyme_score_list[1]==2) or (len(lines) == 3 and rhyme_score_list[0] == 2):
                rhyme_score = 1
            else:
                rhyme_score = round(rhyme_score_list[0])/len(lines)
    except: pass
    return len_score, tone_score, rhyme_score
# ------------------------------------------5 CHU---------------------------------------------------
def check_rule_5_chu(stanza: str):
    lines = stanza.split('\n')
    if len(lines)%2 ==0:
        len_score = stanza_len_score(lines,5,5)/len(lines)
    else:
        len_score = stanza_len_score(lines,5,5)/(len(lines)+1)
    tone_score = 0
    rhyme_score = 0
    tone_group = []
    rhyme_group = []
    for line in lines:
        words = line.split(' ')
        # append every 2nd and 4th word to tone_group
        # append every 5th word to rhyme_group
        try:
            tone_group.append(words[1])
        except: tone_group.append('')
        try:
            tone_group.append(words[3])
        except: tone_group.append('')
        try:
            rhyme_group.append(words[4])
        except: pass
    try:
        tone_score = tone_score + stanza_tone_score_45(tone_group)/len(lines)
    except: pass
    try:
        if len(lines) <= 1:
            rhyme_score = 0
        else:
            rhyme_score_list = stanza_rhyme_score_457(rhyme_group, len(lines))
            if rhyme_score_list[0]>=3 or (len(lines) == 4 and rhyme_score_list[0]==2 and rhyme_score_list[1]==2) or (len(lines) == 3 and rhyme_score_list[0] == 2):
                rhyme_score = 1
            else:
                rhyme_score = round(rhyme_score_list[0]) / len(lines)
    except:
        pass
    return len_score, tone_score, rhyme_score
# ------------------------------------------LUC BAT---------------------------------------------------
def check_rule_luc_bat(stanza: str):
    lines = stanza.split('\n')
    if len(lines)%2 ==0:
        len_score = stanza_len_score(lines,6,8)/len(lines)
    else:
        len_score = stanza_len_score(lines,6,8)/(len(lines)+1)
    tone_score = 0
    rhyme_score = 0
    tone_group_6 = [] # B-T-B
    tone_group_8 = [] # B-T-B-B

    prev_8th_word = '' # # chữ 8th hàng bát trước (phải vần chữ 6th hàng lục sau và 6th hàng bát sau)
    numth = 0
    for line in lines:
        words = line.split(' ')
        if numth%2 == 0: # Currently at 6-line
            rhyme_score_step_6 = 0 # there may not be an 8-line
            rhyme_score_step_8 = 0 # so calculate at 6-line first, then 8, take whichever higher

            rhyme_group = []
            if prev_8th_word != '':
                rhyme_group.append(prev_8th_word)
                prev_8th_word = '' # Mỗi lần append thì reset lại


            # append every 2nd, 4th, 6th word to tone_group_6
            try:
                tone_group_6.append(words[1])
            except: tone_group_6.append('')
            try:
                tone_group_6.append(words[3])
            except: tone_group_6.append('')
            try:
                tone_group_6.append(words[5])
                rhyme_group.append(words[5])
            except: tone_group_6.append('')
            try: # rhyme score at 6-line
                rhyme_score_list = stanza_rhyme_score(rhyme_group)
                if numth==0: # Cặp thơ đầu tiên, prev_8th_word chưa tồn tại
                    rhyme_score_step_6 = rhyme_score_list[0]/2
                else: # từ đây đã có prev_8th_word rồi
                    rhyme_score_step_6 = rhyme_score_list[0]/3
            except: pass

            #print(rhyme_score_list)
            rhyme_score += rhyme_score_step_6
        else:
            # append every 2nd, 4th, 6th, 8th word to tone_group_8
            try:
                tone_group_8.append(words[1])
            except: tone_group_8.append('')
            try:
                tone_group_8.append(words[3])
            except: tone_group_8.append('')
            try:
                tone_group_8.append(words[5])
                rhyme_group.append(words[5])
            except: tone_group_8.append('')
            try:
                tone_group_8.append(words[7])
                prev_8th_word = words[7]
            except:
                tone_group_8.append('')
                prev_8th_word = ''
            try: # rhyme score at 8-line
                rhyme_score_list = stanza_rhyme_score(rhyme_group)
                if numth==1: # Cặp thơ đầu tiên, prev_8th_word ko tồn tại
                    rhyme_score_step_8 = rhyme_score_list[0]/2
                else: # từ đây đã có prev_8th_word r
                    rhyme_score_step_8 = rhyme_score_list[0]/3
            except: pass

            #print(rhyme_score_list)
            # nếu step 8 lớn hơn thì cộng vào bù step 6 ra
            rhyme_score = rhyme_score - rhyme_score_step_6 + max(rhyme_score_step_6,rhyme_score_step_8)

        numth+=1

    try:
        tone_score = tone_score + stanza_tone_score_68(tone_group_6, tone_group_8)/len(lines)
    except: pass
    if len(lines) == 1:
        rhyme_score = 0
    else:
        if len(lines)%2 ==0 :
            rhyme_score = rhyme_score / (len(lines)/2)
        else:
            rhyme_score = rhyme_score / ((len(lines)+1)/2)
    return len_score, tone_score, rhyme_score
# ------------------------------------------7 CHU---------------------------------------------------
def check_rule_7_chu_4line(stanza: str, rule = ''):
    lines = stanza.split('\n')
    if len(lines) % 2 == 0:
        len_score = stanza_len_score(lines, 7, 7) / len(lines)
    else:
        len_score = stanza_len_score(lines, 7, 7) / (len(lines) + 1)
    tone_score = 0
    rhyme_score = 0
    tone_group = []
    rhyme_group = []

    for line in lines:
        words = line.split(' ')
        # append every 2nd, 4th, 6th, 7th word to tone_group
        # append every 7th word to rhyme_group
        try:
            tone_group.append(words[1])
        except: tone_group.append('')
        try:
            tone_group.append(words[3])
        except: tone_group.append('')
        try:
            tone_group.append(words[5])
        except: tone_group.append('')
        try:
            tone_group.append(words[6])
            rhyme_group.append(words[6])
        except: tone_group.append('')
    try:
        tone_score_, rule = stanza_tone_score_7(tone_group, rule)
        tone_score_ = tone_score_/len(lines)
        tone_score += tone_score_
        #print(rule)
    except: pass

    try:
        if len(lines) == 1: rhyme_score = 0
        else:
            rhyme_score_list = stanza_rhyme_score_457(rhyme_group, len(lines))
            if rhyme_score_list[0]>=3 or (len(lines) == 4 and rhyme_score_list[0]==2 and rhyme_score_list[1]==2) or (len(lines) == 3 and rhyme_score_list[0] == 2):
                rhyme_score = 1
            else:
                rhyme_score = round(rhyme_score_list[0])/len(lines)
    except: pass

    return len_score, tone_score, rhyme_score, rule

def check_rule_7_chu_unlimited(poem: str):
    rule = ''
    count = 0
    poem = poem.split('\n')

    len_score = 0
    tone_score = 0
    rhyme_score = 0

    for n in range(0, len(poem), 4):
        stanza = preprocess_stanza('\n'.join(poem[n:n + 4]))
        count += 1
        len_score_, tone_score_, rhyme_score_, rule = check_rule_7_chu_4line(stanza,rule)
        len_score += len_score_
        tone_score += tone_score_
        rhyme_score += rhyme_score_

    return len_score/count, tone_score/count, rhyme_score/count
# ------------------------------------------8 CHU---------------------------------------------------

def check_rule_8_chu(stanza: str):
    lines = stanza.split('\n')
    if len(lines) % 2 == 0:
        len_score = stanza_len_score(lines, 8, 8) / len(lines)
    else:
        len_score = stanza_len_score(lines, 8, 8) / (len(lines) + 1)
    tone_score = 0
    rhyme_score = 0
    tone_groups = []
    rhyme_group = []
    for line in lines:
        tone_group = []
        words = line.split(' ')
        # append every 3rd, 5th, 6th, 8th word to tone_group
        # append every 7th word to rhyme_group
        try:
            tone_group.append(words[2])
        except:
            tone_group.append('')
        try:
            tone_group.append(words[4])
        except:
            tone_group.append('')
        try:
            tone_group.append(words[5])
        except:
            tone_group.append('')
        try:
            tone_group.append(words[7])
            rhyme_group.append(words[7])
        except:
            tone_group.append('')
            rhyme_group.append('')
        tone_groups.append(tone_group)

    try:
        tone_score += max_tone_score_8_chu(tone_groups)/len(tone_groups)
    except: pass
    try:
        rhyme_score += stanza_rhyme_score_8(rhyme_group)
    except: pass

    return len_score, tone_score, rhyme_score


# ------------------------------------------MAIN FUNCTIONS---------------------------------------------------
def calculate_stanza_score(stanza: str, genre: str):
    if genre == '4 chu':
        return check_rule_4_chu(stanza)
    elif genre == '5 chu':
        return check_rule_5_chu(stanza)
    elif genre == 'luc bat':
        return check_rule_luc_bat(stanza)
    elif genre == '7 chu':
        return check_rule_7_chu_unlimited(stanza)
    else:
        return check_rule_8_chu(stanza)

# determine percentage
def score_sum(stanza: str, genre: str):
    len_score, tone_score, rhyme_score = calculate_stanza_score(stanza, genre)
    return len_score*0.1 + tone_score*0.3 + rhyme_score*0.6

# ---THE MAIN FUNCTION---
def calculate_score(poem: str, genre: str):
    """
       A function to calculate score for a poem that may have some stanzas
       param sentence: poem
       genre: if not specified, will perform classification
       return: score  after checked by rule and calculated by length, tone, and rhyme score (sum them up equally, for now)
     """
    try:
        poem = preprocess_linebreaks(poem)
        sum_ = 0
        count = 0
        for i in poem.split("\n\n"):
            if genre == '4 chu' or genre == '5 chu':
                i = i.split('\n')
                for n in range(0, len(i), 4):
                    # Every stanza is 4-line
                    stanza = preprocess_stanza('\n'.join(i[n:n + 4]))
                    count += 1
                    sum_ = sum_ + score_sum(stanza, genre)
            else:
                stanza = preprocess_stanza(i)
                count += 1
                sum_ = sum_ + score_sum(stanza, genre)

        #print(sum_/count)
    except:
        return 0,''
    return sum_/count, genre

class PoemClassifier:
    def __init__(self):
        self.__classifier = pipeline("text-classification", model='Anshler/vietnamese-poem-classifier')
    def __count_per_lines(self, text):
        text = text.split('\n')
        return str([len(x.split()) for x in text])
    def predict(self,poem):
        if type(poem) is not list and type(poem) is not pd.Series and type(poem) is not str:
            raise TypeError('Must be either str, list[str] or Series(Panda)')
        if type(poem) is str:
            poem = [poem]
        poem = pd.Series(poem).astype(str) # convert to Series
        poem_processed = poem.apply(lambda x: self.__count_per_lines(x)) # convert to word count format like: "[6,8,6,8,6,8]"
        poem = list(poem)
        result = self.__classifier(list(poem_processed))
        return [{'label': result[i]['label'], 'confidence': result[i]['score'], 'poem_score': calculate_score(poem[i], result[i]['label'])[0]} for i in range(len(result))]

