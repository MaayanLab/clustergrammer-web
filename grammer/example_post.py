import re
import cookielib, urllib2, urllib
import poster
import sys
import os

def EnrichrLink(genesStr,clusterInfo=''):
    #post a gene list to enrichr server and get the link.
    cj = cookielib.CookieJar()
    opener = poster.streaminghttp.register_openers()
    opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

    params = {'list':genesStr,'description':clusterInfo}
    datagen, headers = poster.encode.multipart_encode(params)
    url = "http://amp.pharm.mssm.edu/Enrichr/enrich"
    request = urllib2.Request(url, datagen,headers)
    urllib2.urlopen(request)


    x = urllib2.urlopen("http://amp.pharm.mssm.edu/Enrichr/share")
    responseStr = x.read()
    splitPhrases = responseStr.split('"')
    linkID = splitPhrases[3]
    shareUrlHead = "http://amp.pharm.mssm.edu/Enrichr/enrich?dataset="
    enrichrLink = shareUrlHead + linkID
    return enrichrLink

def readperdiff(path):
    #ignore empty file
    if os.path.getsize(path) < 1000:
        print 'Empty file:'+path+'\n'
        return

    print 'Processing:'+path
    
    baseName = os.path.basename(path);
    fileName = os.path.splitext(baseName)[0];
    dirName = os.path.dirname(path);
    if dirName == '':
        dirName = os.getcwd()
    writeDir = dirName +'\\'+'EnrichrLinks';
    if not os.path.exists(writeDir):
        os.makedirs(writeDir)

    f = open(path)
    content = f.read()
    f.close()
    lines = re.split('\n',content)
    linesCount = len(lines)

    #remove vacant lines at the tail of the file if any
    while len(lines[linesCount-1])<100:
        lines.pop()
        linesCount = linesCount-1
        if linesCount == 0:
            break

    
    header = lines[0]
    dat = [lines[i] for i in range(1,linesCount)]

    header = re.split('\t',header)
    dat = [re.split('\t',datum) for datum in dat]

    #Filter out significant rows
    sigMetaIdx = header.index('significant')
    sigDat = [ row for row in dat if row[sigMetaIdx] == 'yes']

    #seperate significant rows into different comparison groups
    sample1MetaIdx = header.index('sample_1')
    sample2MetaIdx = header.index('sample_2')
    comparisons = []
    comparisonsDat = []
    for row in sigDat:
        rowComparison = [row[sample1MetaIdx],row[sample2MetaIdx]]
        if rowComparison not in comparisons:
            comparisons.append(rowComparison)
            comparisonsDat.append([])
        comparisonsIdx = comparisons.index(rowComparison)
        comparisonsDat[comparisonsIdx].append(row)

    #seperate rows in each comparison goup into up and down subgroup
    log2FoldMetaIdx = header.index('log2(fold_change)')
    comparisonsUpDat = [[row for row in perComparisonDat
                         if float(row[log2FoldMetaIdx])>0]
                        for perComparisonDat in comparisonsDat]
    comparisonsDownDat = [[row for row in perComparisonDat
                           if float(row[log2FoldMetaIdx])<0]
                          for perComparisonDat in comparisonsDat]

    #extract genes in each subgroup
    geneMetaIdx = header.index('gene')
    comparisonsUpGenes = [ [row[geneMetaIdx] for row in perComparisonUpDat]
                           for perComparisonUpDat in comparisonsUpDat]
    comparisonsDownGenes = [[row[geneMetaIdx] for row in perComparisonDownDat]
                            for perComparisonDownDat in comparisonsDownDat]


    #enrichr post and write the response links into txt file
    comparisonsCount = len(comparisons)
    wStr = ''
    for i in range(comparisonsCount):
        upInfo = comparisons[i][0]+','+comparisons[i][1]+'\tUp Genes'
        if len(comparisonsUpGenes[i])==0:
            upLink = ''
        else:
            for j in range(len(comparisonsUpGenes[i])):
                perGene = comparisonsUpGenes[i][j]
                match = re.search(r'[\w\-@./]+',perGene)
                if match.group(0) is not perGene:
                    print '"' + perGene + '"' + ' is not a valid gene symbol and converted to ' + '"' + match.group(0) + '"'
                    comparisonsUpGenes[i][j] = match.group(0)
                    
            upLink = EnrichrLink('\n'.join(comparisonsUpGenes[i]), upInfo)
        
        downInfo = comparisons[i][0]+','+comparisons[i][1]+'\tDown Genes'
        if len(comparisonsDownGenes[i]) == 0:
            downLink = ''
        else:
            for j in range(len(comparisonsDownGenes[i])):
                perGene = comparisonsDownGenes[i][j]
               
                match = re.search(r'[\w\-@./]+',perGene)
                if match.group(0) is not perGene:
                    
                    print '"' + perGene + '"' + ' is not a valid gene symbol and converted to ' + '"' + match.group(0)+ '"'
                    comparisonsDownGenes[i][j] = match.group(0)
                    
            downLink = EnrichrLink('\n'.join(comparisonsDownGenes[i]), downInfo)
        
        wStr = wStr + upInfo+'\t'+ upLink +'\n'
        wStr = wStr + downInfo+ '\t' + downLink+'\n'
                
    f = open(writeDir+'\\'+fileName+'_enrichrLinks.txt','w')
    f.write(wStr)
    f.close()


    #below is printing up and down genes of each comparison to a single txt file
    rowMax = 0
    for perComparisonUpGenes in comparisonsUpGenes:
        if rowMax < len(perComparisonUpGenes):
            rowMax = len(perComparisonUpGenes)
            
    for perComparisonDownGenes in comparisonsDownGenes:
        if rowMax < len(perComparisonDownGenes):
            rowMax = len(perComparisonDownGenes)

    colMax = 2*len(comparisons)
    wStr = ''
    for i in range(colMax):
        if i%2 == 0:
            wStr = wStr + comparisons[i/2][0]+','+ comparisons[i/2][1]+'\t'
        else:
            wStr = wStr + '\t'
    wStr.rstrip('\t')
    wStr =wStr + '\n'

    secondRow = '\t'.join(['Up Genes','Down Genes']*(colMax/2))
    wStr = wStr + secondRow + '\n'

    for i in range(rowMax):
        for j in range(len(comparisons)):
            try :
                wStr = wStr + comparisonsUpGenes[j][i] + '\t'
            except IndexError:
                wStr = wStr + '\t'
            try :
                wStr = wStr + comparisonsDownGenes[j][i] + '\t'
            except IndexError:
                wStr = wStr + '\t'
        wStr.rstrip('\t')
        wStr =wStr + '\n'

    f = open(writeDir+'\\'+fileName+'_updown.txt','w')
    f.write(wStr)
    f.close()
    print '\n'
    
def readdiff(path):
    print '\n'
    if os.path.isfile(path):
         readperdiff(path)
    else:
        for directory, dirnames,filenames in os.walk(path):
            [readperdiff(directory+'\\'+perFile) for perFile in filenames
             if os.path.splitext(perFile)[1] == '.diff']

arg = sys.argv
if len(arg) == 1:
    arg.append(os.getcwd())
readdiff(arg[1])
