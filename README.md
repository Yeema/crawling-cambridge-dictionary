# crawling-cambridge-dictionary
<h2>cambridge.urls.py</h2> 
  
  1. cmd: python cambridge.urls.py
  2. goal: used to capture all urls in https://dictionary.cambridge.org/browse/english-chinese-traditional/
  3. implementation:
     1. got guideurls by appending https://dictionary.cambridge.org/browse/english-chinese-traditional/ from a to z
     2. got extendurls by capturing urls from each guideurls
  
<h2>cambridge.dictionary.py</h2>
  
  1. cmd: python cambridge.dictionary.py
  2. goal: crawled all pages in cambridge dictionary
  3. implementation:
     1. accese extendurls and preprocessed html
