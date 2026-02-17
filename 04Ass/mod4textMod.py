import pandas as pd
import string
import re
import contractions
import nltk
import multidict
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

print(
    "From Kaggle, I used a dataset containing reviews for phones and accessories from amazon"
)  # https://www.kaggle.com/datasets/abdallahwagih/amazon-reviews
file = r"./Mod4-Support-Files/amazonReviews/Cell_Phones_and_Accessories_5.json"

df = pd.read_json(file, lines=True)

wordnet_lemmatizer = WordNetLemmatizer()
stopwords_list = stopwords.words("english")


def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text


def remove_stopwords(text):
    output = [i for i in text if i not in stopwords_list]
    return output


def remove_punctuation(text):
    punctuationfree = "".join([i for i in text if i not in string.punctuation])
    return punctuationfree


def tokenization(text):
    tokens = text.split()
    return tokens


def untokenization(item):
    remWords = " ".join(item)
    return remWords


df["clean_text"] = df["reviewText"].astype(str).apply(lambda x: x.lower())
df["clean_text"] = df["clean_text"].apply(lambda x: contractions.fix(x))
df["clean_text"] = df["clean_text"].apply(lambda x: remove_punctuation(x))
df["clean_text"] = df["clean_text"].apply(lambda x: re.sub(r"\w*\d\w*", "", x))
df["clean_tokenized"] = df["clean_text"].apply(lambda x: tokenization(x))
df["clean_tokenized"] = df["clean_tokenized"].apply(lambda x: remove_stopwords(x))
df["clean_tokenized"] = df["clean_tokenized"].apply(lambda x: lemmatizer(x))
df["cleanText"] = df["clean_tokenized"].apply(lambda x: untokenization(x))


print("\nSentiment Analysis\n\n")
sid = SentimentIntensityAnalyzer()

df["sentiment_score"] = df["cleanText"].apply(
    lambda x: sid.polarity_scores(x)["compound"]
)
print("Overall Sentiment Average:", df["sentiment_score"].mean())

subgroups = [1, 2, 4, 5]
for rating in subgroups:
    sub_df = df[df["overall"] == rating]
    avg_score = sub_df["sentiment_score"].mean()
    print(f"Star Rating {rating}: Average Sentiment = {avg_score:.4f}")


def getFrequencyDictForText(Item):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    for text in Item.split(" "):
        val = tmpDict.get(text, 0)
        tmpDict[text] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict


def makeImage(text, title="Word Cloud"):
    wc = WordCloud(background_color="white", max_words=100)
    wc.generate_from_frequencies(text)

    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show()


def generate_filtered_cloud(df_input, title_str):
    print(f"Generating {title_str}...")
    text = " ".join(df_input["cleanText"])

    text = re.sub(r"[^a-zA-Z ]", "", text)

    myDict = getFrequencyDictForText(text)
    if "" in myDict:
        myDict.pop("")

    mylist = dict(sorted(myDict.items(), key=operator.itemgetter(1), reverse=True))
    for item in list(mylist.items()):
        if item[1] <= 3:
            if item[0] in myDict:
                myDict.pop(item[0])

    mylist = dict(sorted(myDict.items(), key=operator.itemgetter(1), reverse=True))
    for item in list(mylist.items()):
        if len(item[0]) <= 4:
            if item[0] in myDict:
                myDict.pop(item[0])

    common_words = [
        "phone",
        "product",
        "amazon",
        "would",
        "battery",
        "charge",
        "case",
        "item",
        "work",
        "screen",
    ]
    for word in common_words:
        if word in myDict:
            myDict.pop(word)

    if len(myDict) > 0:
        makeImage(myDict, title=title_str)
    else:
        print(f"Not enough words remaining for {title_str}")


generate_filtered_cloud(df, "Overall Word Cloud")

df_1_star = df[df["overall"] == 1]
generate_filtered_cloud(df_1_star, "Word Cloud: 1-Star Reviews")

df_5_star = df[df["overall"] == 5]
generate_filtered_cloud(df_5_star, "Word Cloud: 5-Star Reviews")

df["reviewTime"] = pd.to_datetime(df["reviewTime"], format="%m %d, %Y")

df["year"] = df["reviewTime"].dt.year
df["month"] = df["reviewTime"].dt.month
df["day"] = df["reviewTime"].dt.day
df["day_of_week"] = df["reviewTime"].dt.day_name()

print("First 5 rows with new Date columns:")
print(df[["reviewTime", "year", "month", "day", "day_of_week"]].head())

target_word = "battery"

df_target = df[
    df["reviewText"].astype(str).str.contains(target_word, case=False, na=False)
]

print(f"\nTotal reviews mentioning '{target_word}': {len(df_target)}")

counts_by_year = df_target["year"].value_counts().sort_index()

print(f"\nFrequency of the word '{target_word}' by Year:")
print(counts_by_year)
