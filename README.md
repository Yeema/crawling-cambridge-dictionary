# crawling-cambridge-dictionary
<h2>cambridge.urls.py</h2> 
  
  1. cmd: python cambridge.urls.py
  2. used to capture all urls in https://dictionary.cambridge.org/browse/english-chinese-traditional/
  3. got guideurls by appending https://dictionary.cambridge.org/browse/english-chinese-traditional/ from a to z
  4. got extendurls by capturing urls from each guideurls
  
<h2>cambridge.dictionary.py</h2>
  
  1. cmd: python cambridge.dictionary.py
  2. crawled all pages in cambridge dictionary
  3. accese extendurls and preprocessed html
