import pandas as pd
import csv
import os
import scipy.sparse

# Preprocesing
import preprocessor as prepro
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
from nltk.stem import PorterStemmer
import nltk

# Metrics
from sklearn.metrics import silhouette_score

# Algorithms
from sklearn.cluster import KMeans

#-----------------------------------------------------------------------------#
#                        FUNCTIONS FOR TEXT PREPROCESING
def strip_punctuation(s):
    """ Remove punctuation from the string s. """
    return ''.join(c for c in s if c not in punctuation)

def remove_stopwords(s):
    """ Remove stop words from the string s."""
    words = word_tokenize(s)
    stop_words = set(stopwords.words('english'))
    words_filtered = []
    for w in words:
        if w not in stop_words:
            words_filtered.append(w)
            
    return ' '.join(words_filtered)

def to_lower(s):
    """ Change to lower case all the words from s. """
    return ''.join(word.lower() for word in s)

def remove_weird_words(s):
    english_words = set(nltk.corpus.words.words())
    
    filtered = []
    for word in s.split():
        if word in english_words:
            filtered.append(word)
            
    return ' '.join(filtered)

def remove_numbers(s):
    """ Remove numbers from s. """
    return ' '.join(word for word in s.split() if not word.isdigit())

def stemming(s):
    ps = PorterStemmer()
    stems = []
    for word in s.split():
        stems.append(ps.stem(word))
        
    return ' '.join(stems)

def preprocess_text(s):
    s = to_lower(s)
    s = remove_numbers(s)
    s = strip_punctuation(s)
    s = remove_stopwords(s)
    s = remove_weird_words(s)
    s = stemming(s)
    return s
            
#-----------------------------------------------------------------------------#
#                             LOADING THE DATA
path = "C://Users//Yus//Desktop//gitSI//Twitter-Clustering"
os.chdir(path)

# Set data files' paths
avengers_path = path+"//avengers_tweets.csv"
bp_path = path+"//bp_tweets.csv"
venom_path = path+"//venom_tweets.csv"

# Load csv
avengers_data = pd.read_csv(avengers_path, sep = ',', names = None)
bp_data = pd.read_csv(bp_path, sep = ',', names = None)
venom_data = pd.read_csv(venom_path, sep = ',', names = None)

# Add tags to know the origin of the tweet
avengers_data["Tag"] = 0  # "Avengers"
bp_data["Tag"] = 1  # "BlackPanther"
venom_data["Tag"] = 2  # "Venom"

# Rename first column
avengers_data.columns =  ['Tweet','Tag']
bp_data.columns =  ['Tweet','Tag']
venom_data.columns =  ['Tweet','Tag']

# Get the corpus of each tag
text_av = list(avengers_data.iloc[:,0])
text_bp = list(bp_data.iloc[:,0])
text_venom = list(venom_data.iloc[:,0])
#
##-----------------------------------------------------------------------------#
#                            PREPROCESSING DATA

# Clean the text of each document
for i in range(0, len(text_av)):
    text_av[i] = preprocess_text(text_av[i])    
    
for i in range(0, len(text_bp)):
    text_bp[i] = preprocess_text(text_bp[i])

for i in range(0, len(text_venom)):
    text_venom[i] = preprocess_text(text_venom[i])

all_documents = text_av + text_bp + text_venom 

#with open("clean_av.csv",'wb') as file:
#    writer = csv.writer(file)
#    for elem in text_av:
#        writer.writerow(str(elem))
#        
#with open("clean_bp.csv",'wb') as file:
#    writer = csv.writer(file)
#    for elem in text_bp:
#        writer.writerow([elem.encode('utf-8')])        
#        
#with open("clean_venom.csv",'wb') as file:
#    writer = csv.writer(file)
#    for elem in text_venom:
#        writer.writerow([elem.encode('utf-8')])
     
#-----------------------------------------------------------------------------#
#               CREATE THE DOC-TERM MATRIX, CALCULATE TF-IDF
# Doc-term matrix 
tokenize = lambda doc: doc.lower().split(" ")

# Define tfidf transformation
sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True,
                                smooth_idf=False, sublinear_tf=True, 
                                tokenizer=tokenize)

# Calculate Document-term Matrix with tf-idf 
tfidf_matrix = sklearn_tfidf.fit_transform(all_documents)

terms = sklearn_tfidf.get_feature_names()
dist = 1 - cosine_similarity(tfidf_matrix)

# SAVE TFIDF
# scipy.sparse.save_npz('D://sparse_matrix.npz', tfidf_matrix)

# LOAD TFIDF
#tfidf_matrix = scipy.sparse.load_npz('D://sparse_matrix.npz') 


#-----------------------------------------------------------------------------#
#                           CLUSTERING ALGORITHMS

#K-means

# Probamos diferentes valores de k clusters objetivos
k_clusters = [3,4,5,6,7,8,9,10]
for k in k_clusters:
    km = KMeans(n_clusters=k)
    km.fit(tfidf_matrix)
    clusters = km.labels_.tolist()
    # Silhouette score
    silhouette = silhouette_score(tfidf_matrix, clusters)
    print("Silhouette score para k =",k,silhouette)

