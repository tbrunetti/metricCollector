import argparse
import pandas
import os

from pandas._config import config

def combine():
    pass

def starLogs(config, outdir, metricLibrary):
    
    starMetrics = {}
    toProcess = [[name, loc] for name,loc in zip(config['sampleName'],config['starLogs'])]
    for logs in toProcess:
        starMetrics[logs[0]] = {}
        with open(logs[1], 'r') as metrics:
            for line in metrics:
                line = line.split('|')
                if len(line) != 2:
                    continue
                else:
                    line[0] = line[0].strip()
                    line[1] = line[1].strip()
                    starMetrics[logs[0]][line[0]] = line[1]
    
    combinedMetrics = pandas.DataFrame.from_dict(starMetrics, orient='index')
    combinedMetrics['sampleName'] = combinedMetrics.index
    
    metricLibrary.append(combinedMetrics)

    #combinedMetrics.to_csv(os.path.join(outdir, filename), sep = '\t', index = False)
    
    return metricLibrary


def picardRNA(config, outdir, metricLibrary):
    
    picardRNAmetrics = {}
    toProcess = [[name, loc] for name,loc in zip(config['sampleName'], config['picardRNA'])]
    for logs in toProcess:
        with open(logs[1], 'r') as metrics:
            for line in metrics:
                if line.startswith('PF_BASES'): # look for header
                    keyNames = line.strip().split('\t')
                    values = next(metrics).strip().split('\t') # following header get next line in metrics file
                    picardRNAmetrics[logs[0]] = dict(zip(keyNames, values)) # pair key value lists into dictionary and store as dict of dicts
                    # note next() should automatically exit loop
        
    combinedMetrics = pandas.DataFrame.from_dict(picardRNAmetrics, orient = 'index')
    combinedMetrics['sampleName'] = combinedMetrics.index
    
    metricLibrary.append(combinedMetrics)
    
    return metricLibrary
                                        
def picardAlignment(config, outdir, metricLibrary):
    pass

def picardInsertSize(config, outdir, metricLibrary):
    picardInsertSizemetrics = {}
    toProcess = [[name, loc] for name,loc in zip(config['sampleName'], config['picardInsertSize'])]
    for logs in toProcess:
        with open(logs[1], 'r') as metrics:
            for line in metrics:
                if line.startswith('MEDIAN_INSERT_SIZE'): # look for header
                    keyNames = line.strip().split('\t')
                    values = next(metrics).strip().split('\t') # following header get next line in metrics file
                    picardInsertSizemetrics[logs[0]] = dict(zip(keyNames, values)) # pair key value lists into dictionary and store as dict of dicts
                    # note next() should automatically exit loop
        
    combinedMetrics = pandas.DataFrame.from_dict(picardInsertSizemetrics, orient = 'index')
    combinedMetrics['sampleName'] = combinedMetrics.index
    
    metricLibrary.append(combinedMetrics)
    
    return metricLibrary

def picardMarkDups(config, outdir, metricLibrary):
    
    picardDupsMetrics = {}
    toProcess = [[name, loc] for name,loc in zip(config['sampleName'], config['picardMarkDups'])]
    for logs in toProcess:
        with open(logs[1], 'r') as metrics:
            for line in metrics:
                if line.startswith('LIBRARY'): # look for header
                    keyNames = line.strip().split('\t')
                    values = next(metrics).strip().split('\t') # following header get next line in metrics file
                    picardDupsMetrics[logs[0]] = dict(zip(keyNames, values)) # pair key value lists into dictionary and store as dict of dicts
                    # note next() should automatically exit loop
        
    combinedMetrics = pandas.DataFrame.from_dict(picardDupsMetrics, orient = 'index')
    combinedMetrics['sampleName'] = combinedMetrics.index
    
    metricLibrary.append(combinedMetrics)
    
    return metricLibrary


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A piece of code to concatenate different metrics into a large metrics file for downstream analysis.')
    parser.add_argument('--config', required=True, help='A tab-delimited files containing the location of all metric files for each sample.')
    parser.add_argument('--metrics', help='Comma-separated list of all metrics to combine.  Options include: starLogs, picardRNA, picardAlignment, pircardInsertSize, picardMarkDups')
    parser.add_argument('--outdir', default=os.getcwd(), help='Path to output directory (must already exist)')
    parser.add_argument('--filename', default='metricCollector.out', help='Name of output file')
    args = parser.parse_args()
    
    configDf = pandas.read_csv(args.config, header=0, delimiter = '\t')
    listOfDfs = []
    
    '''
    TODO
    check that directory path exists
    check config header with proper names exist
    check metrics listed are valid options
    '''
        
    if args.metrics == 'starLogs':
        listOfDfs = starLogs(config = configDf, outdir = args.outdir, filename = args.filename, metricLibrary = listOfDfs)
    
    if args.metrics == 'picardRNA':
        listOfDfs = picardRNA(config = configDf, outdir = args.outdir, metricLibrary = listOfDfs)
    
    if args.metrics == 'picardInsertSize':
        listOfDfs = picardInsertSize(config = configDf, outdir = args.outdir, metricLibrary = listOfDfs)
        
    if args.metrics == 'picardMarkDups':
        listOfDfs = picardMarkDups(config = configDf, outdir = args.outdir, metricLibrary = listOfDfs)
        
    if args.metrics == 'picardAlignment':
        listOfDfs = picardAlignment(config = configDf, outdir = args.outdir, metricLibrary= listOfDfs)