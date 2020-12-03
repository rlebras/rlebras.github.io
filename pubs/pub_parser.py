from xml.dom import minidom

def getNodeText(node):

    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

conf_fullname_map = {
    'AAAI': 'Conference on Artificial Intelligence',
    'CompSust': 'International Conference on Computational Sustainability',
    'CP': 'International Conference on Principles and Practice of Constraint Programming',
    'CP-AI-OR': 'International Conference on Integration of Artificial Intelligence and Operations Research Techniques in Constraint Programming',
    'IAAI': 'Conference on Innovative Applications of Artificial Intelligence',
    'IJCAI': 'International Joint Conference on Artificial Intelligence',
    'J Econ Behav Organ.': 'The Journal of Economic Behavior and Organization',
    'EMNLP': 'Empirical Methods in Natural Language Processing',
    'Findings of EMNLP': 'Empirical Methods in Natural Language Processing',
    'HCOMP': 'AAAI Conference on Human Computation and Crowdsourcing',
    'ICLR': 'International Conference on Learning Representations',
    'ICML': 'International Conference on Machine Learning',
    'SAT': 'International Conference on Theory and Applications of Satisfiability Testing',
    'SemEval-NAACL': 'North American Chapter of the Association for Computational Linguistics',
    'The VLDB Journal': 'The International Journall on Very Large Data Bases',
    'VLDB': 'International Conference on Very Large Data Bases',
}

journals=['The VLDB Journal', 'J Econ Behav Organ.']

def getConfName(conf, year):
    ret = conf + " " + year
    if conf in conf_fullname_map:
        ret = conf_fullname_map[conf] + ", " + ret
    return ret


def writeHTML(paper, link, authors, year, conf, abstract):
    type='cpaper ' + conf
    s='''<div class="item mix TYPEPH" data-year="YEARPH">
                                                    <div class="pubmain">
                                                        <div class="pubassets">

                                                            <a href="#" class="pubcollapse">
                                                                <i class="fa fa-expand"></i>
                                                            </a>
                                                            <a href="LINKPH" title="Download" target="_blank">

                                                                <i class="fa fa-external-link"></i>
                                                            </a>
                                                        </div>

                                                        <h4 class="pubtitle">PAPERPH</h4>
                                                        <div class="pubauthor">AUTHORSPH</div>
                                                        <div class="pubauthor">
                                                        </div>
                                                        <div class="pubcite"><span class="label label-success">CONFPH</span> CONFFULLPH </div>

                                                    </div>
                                                    <div class="pubdetails">
                                                        <h4>Abstract</h4>
                                                        <p>ABSTRACTPH</p>
                                                    </div>
        </div>'''
    if conf in journals:
        type="jpaper " + conf
    s = s.replace('TYPEPH', type)
    s = s.replace('PAPERPH', paper)
    s = s.replace('LINKPH', link)
    s = s.replace('AUTHORSPH', authors)
    s = s.replace('YEARPH', year)
    s = s.replace('CONFPH', conf)
    s = s.replace('CONFFULLPH', getConfName(conf, year))
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
        conf_year=clean(getNodeText(s.getElementsByTagName('BodySmall')[1]))
        conf=clean(conf_year.split("|")[0])
        year=clean(conf_year.split("|")[1])
        abstract=getNodeText(s.getElementsByTagName('p')[0])
        link=title.getAttribute("href").strip()
        paper=clean(getNodeText(title))

        s = writeHTML(paper, link, authors, year, conf, abstract)
        print(s)
        f = open("../publication_items.html", "w")
        f.write(s)
        f.close()

def main():
    parse()

if __name__ == "__main__":
    main()