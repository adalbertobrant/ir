import ssl
import time
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


__cache__ = {}


def busca_preco_atual(ticker):
    if ticker in __cache__:
        return __cache__[ticker]
    else:
        preco = __third_party_lib(ticker)
        if type(preco) is float:
            return preco

        return __custom(ticker)


def __custom(ticker):
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        ticker_sa = ticker + '.SA'
        url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker_sa, ticker_sa)

        # Making the website believe that you are accessing it using a Mozilla browser
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        time.sleep(1)

        soup = BeautifulSoup(webpage, 'html.parser')
        # html = soup.prettify('utf-8')

        for span in soup.findAll('span', attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'}):
            preco_atual = float(span.text.replace(',', '').strip())
            __cache__[ticker] = preco_atual
            return preco_atual
        raise Exception('Preco ticker nao encontrado ' + ticker)
    except Exception as ex:
        raise Exception('Preco ticker nao encontrado ' + ticker, ex)


def __third_party_lib(ticker):
    from requests import sessions
    session = sessions.Session()
    ticker_sa = ticker + '.sa'
    from yahooquery import Ticker
    try:
        preco = Ticker(ticker_sa, session=session).price[ticker_sa]['regularMarketPrice']
    except Exception as ex:
        raise ex
    finally:
        session.close()
    return preco
