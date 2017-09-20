FROM scrapinghub/scrapinghub-stack-scrapy:1.3
ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE Olxscraper.settings
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get -y -q install tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN python setup.py install
