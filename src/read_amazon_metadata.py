import argparse
import gzip
import nltk
import pdb
import sys, os
import re

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

exception_chars = ['|', '/', '\\', '-', '(', ')', '!', ':', ';', '<', '>']

def preprocess(text):
    text = text.replace('|', ' ')
    text = text.replace('/', ' ')
    text = text.replace('\\', ' ')
    text = text.lower()
    #text = re.sub(r'\W+', ' ', text)
    ret_text = ''
    for sent in nltk.sent_tokenize(text):
        ret_text += ' '.join(nltk.word_tokenize(sent)) + ' '
    return ret_text

def main(args):
    products = {}
    given_brand = ''
    sim_prod_brands = []
    for v in parse(args.metadata_fname):
        if 'description' not in v or 'title' not in v:
            continue
        asin = v['asin']
        if asin == 'B0006GQ8J0':
            given_brand = v['brand']
        if asin in 'B0043XYNNA B00006WNSN B00004RC6S B00008IH9R B0000BYBTR B005QOWA44 \
        B005N7BUMW B0018A8THM B000TGNN4K B0000CFSGR B000BK5EBY B001CHIFDO B0036WS1FA B0088FJSWA \
        B005PO79OQ B000T9XPHC B0000CFSS5 B009HEPAGY B00CW5SQHU B007Q40BOS B0010XECWI B00008IH9X \
        B001AH5H0A B000TK8SLY B000RVG9D4 B0082IY238 B000T9SCZ2 B000153ZYW B00BFJ92YA B008YNFB3Q \
        B000LNRP3G B000BI8EJK B000VP7HQ4 B00023XCV4 B00A89H6X2 B000WPX532 B000LDO4U8 B0034U2PD8 \
        B008BW0M8Y B002JM100Q B00D95CZA6 B00004RC6R B00E58P7ME B0063NHLJQ B0019707DS B00CJ1HF7O \
        B00390T5JA B00AZSZWZA B00AZSZX40 B005NICH5U B008LTIYN2 B002VLYQ42 B000FOBBN6 B004VS54BC \
        B00006IV0Q B005MM7ZE0 B005MM80GM B005MM7ZOU B0081VRKDA B006QG8ITM B002IASYA8 B003O9YUVY \
        B002MZYZHU B000SSMS72 B000AQPMHA B00065L602 B00015NN0S B007B64P7A B00935GWRS B00BUYJBWS \
        B00BN0OWGY B0000A1ZMS B004OSC8OK B00310SB2K B00012XCZW B00CEILY9W B0052TRE26 B0052TSQJG \
        B005M3QVM6 B0000X7CMQ B0009U5NEY B00G3DCUQK B003WTMLS0 B00AZSZYK8 B0036WS1GY B00CJB0M4C \
        B00C4VVLI8 B0002JA1JE B00A157JP8 B0006FU8AG B001QTVS5K B000NKRWNA B000Q94C90 B007ZOC232 \
        B00BFZTUAU B004L173WC B00030J1SE B00422KVY2 B008AK8784'.split():
            print asin
            if 'brand' not in v.keys():
                print 'No brand info'
            else:
                sim_prod_brands.append(v['brand'])            
    print given_brand
    print sim_prod_brands

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--metadata_fname", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)

