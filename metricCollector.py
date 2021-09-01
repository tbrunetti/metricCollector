import argparse
import pandas
import os

def combine():
    pass

def starLogs(config, outdir, filename):
    
    config = pandas.read_csv('/home/tonya/projects/JaredKlarquist_RNAseq_ChEA_mouseGenos_08312021/alignment_metrics/determine_alignment_parameterization/metricCollector_sampleSheet.tsv', header=0, delimiter = '\t')

    starMetrics = {}
    toProcess = [[name, loc] for name,loc in zip(config['sampleName'],config['star_log'])]
    for logs in toProcess:
        print(logs)
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
    
    starCombine = pandas.DataFrame.from_dict(starMetrics, orient='index')
    starCombine.to_csv(os.path.join(outdir, filename), sep = '\t', index = False)

def picardRNA():
    pass

def picardAlignment():
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A piece of code to concatenate different metrics into a large metrics file for downstream analysis.')
    parser.add_argument('--config', required=True, help='A tab-delimited files containing the location of all metric files for each sample.')
    parser.add_argument('--metrics', help='Comma-separated list of all metrics to combine.  Options include: starLogs, picardRNA, picardAlignment')
    parser.add_argument('--outdir', default=os.getcwd(), help='Path to output directory (must already exist)')
    parser.add_argument('--filename', default='metricCollector.out', help='Name of output file')
    args = parser.parse_args()
    
    configDf = pandas.read_csv(args.config, header=True, delimiter = '\t')
    
    '''
    TODO
    check that directory path exists
    check config header with proper names exist
    check metrics listed are valid options
    '''
    
    if args.metrics == 'starLogs':
        starLogs(config = configDf, outdir = args.outdir, filename = args.filename)