# crawling-cambridge-dictionary
<h2>cambridge.urls.py</h2> 
  
  > cmd: python cambridge.urls.py
  1. used to capture all urls in https://dictionary.cambridge.org/browse/english-chinese-traditional/
  2. got guideurls by appending https://dictionary.cambridge.org/browse/english-chinese-traditional/ from a to z
  3. got extendurls by capturing urls from each guideurls
  
<h2>cambridge.dictionary.py</h2>
  
  > python cambridge.dictionary.py
  1. crawled all pages in cambridge dictionary
  2. accese extendurls and preprocessed html
