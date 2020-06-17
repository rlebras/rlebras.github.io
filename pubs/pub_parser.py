from xml.dom import minidom

def getNodeText(node):

    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

def writeHTML(paper, link, authors, year, conf, abstract):
    s='''<div class="item mix cpaper" data-year="YEARPH">
                                                    <div class="pubmain">
                                                        <div class="pubassets">

                                                            <a href="#" class="pubcollapse">
                                                                <i class="fa fa-expand"></i>
                                                            </a>
                                                            <a href="LINKPH" title="Download" target="_blank">

                                                                <i class="fa fa-cloud-download"></i>
                                                            </a>
                                                        </div>

                                                        <h4 class="pubtitle">PAPERPH</h4>
                                                        <div class="pubauthor">AUTHORSPH</div>
                                                        <div class="pubauthor">
                                                        </div>
                                                        <div class="pubcite"><span class="label label-success">Conference Papers</span> ArXiv Pre-Print</div>

                                                    </div>
                                                    <div class="pubdetails">
                                                        <h4>Abstract</h4>
                                                        <p>ABSTRACTPH</p>
                                                    </div>
        </div>'''
    s = s.replace('PAPERPH', paper)
    s = s.replace('LINKPH', link)
    s = s.replace('AUTHORSPH', authors)
    s = s.replace('YEARPH', year)
    s = s.replace('CONFPH', conf)
    s = s.replace('ABSTRACTPH', abstract)
    return s

def clean(s):
    ret = s.strip().replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    return ' '.join(ret.split())

def parse():
    file = "./publication_list.xml"
    xmldoc = minidom.parse(file)
    itemlist = xmldoc.getElementsByTagName('Result.Item')

    for s in itemlist:
        title=s.getElementsByTagName('Result.Title')[0].getElementsByTagName('a')[0]
        authors=clean(getNodeText(s.getElementsByTagName('BodySmall')[0].getElementsByTagName('strong')[0]))
        year_conf=clean(getNodeText(s.getElementsByTagName('BodySmall')[1]))
        year=clean(year_conf.split("|")[0])
        conf=clean(year_conf.split("|")[1])
        abstract=getNodeText(s.getElementsByTagName('p')[0])
        link=title.getAttribute("href").strip()
        paper=clean(getNodeText(title))

        s = writeHTML(paper, link, authors, year, conf, abstract)
        print(s)

def main():
    parse()

if __name__ == "__main__":
    main()