import os
from six.moves import urllib

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/chrisjmccormick/MinHash/master/data"
PLAGIARISM_PATH = "data"
DATA_SIZES = [100,1000,2500,10000]

def fetch_data(download_root=DOWNLOAD_ROOT, 
               path=PLAGIARISM_PATH, 
               maxsize=1000):
  if not os.path.isdir(path):
      os.makedirs(path)
        
  for size in DATA_SIZES:
      if size <= maxsize:
          train_file = "articles_" + str(size) + ".train" 
          train_path = path + '/' + train_file
          if not os.path.exists(train_path):
              train_url = download_root + '/' + train_file
              urllib.request.urlretrieve(train_url, train_path)
          
          truth_file = "articles_" + str(size) + ".truth"
          truth_path = path + '/' + truth_file
          if not os.path.exists(truth_path):
              truth_url = download_root + "/" + truth_file
              urllib.request.urlretrieve(truth_url, truth_path)