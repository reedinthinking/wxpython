#!/usr/bin/env python
# encoding:utf-8
import re
import os
from analysisFile.Scount import Scount
from updateConfig.configOpt import ConfigUtil


class Assemble(object):

    def __init__(self):
        self.abspath = self.getAbsolutePath()
        self.filepath = self.getConfigContent('filepath')
        self.path_raw = self.filepath['inputfile'][:(self.filepath['inputfile'].rfind('/') + 1)]
        self.ref = self.filepath['inputfile'][(self.filepath['inputfile'].rfind('/') + 1):]
        self.outputpath = self.filepath['outputpath']

        self.params = self.getConfigContent('params')
        self.seq_name = self.params['seq_name']
        self.max_run = int(self.params['max_run'])
        self.Blast_ident = int(self.params['Blast_ident'])
        self.threshold = float(self.params['threshold'])

        self.software_path = self.getConfigContent('software')

    def getAbsolutePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print current_dir
        return current_dir

    def getConfigContent(self, key):
        '''return dict :
        '''
        config_path = self.abspath + '/../config/config.ini'
        print "chushi peizhi wenjian*********************"
        print config_path
        myconfig = ConfigUtil(config_path)
        dict = {}
        list = myconfig.get_items(key)
        for item in list:
            dict[item[0]] = item[1]
        return dict

    def runAssemble(self):
        os.mkdir(r'%s/tmp0' % self.outputpath)
        os.mkdir(r'%s/tmp0/megahit_out' % self.outputpath)
        cmd00 = r'cp %s/%s %s/tmp0/megahit_out/final.contigs.fa' % (self.path_raw, self.ref, self.outputpath)
        os.system(cmd00)
        for k in range(0, self.max_run):
            os.mkdir(r'%s/tmp%d' % (self.outputpath, k + 1))
            os.chdir(r'%s/tmp%d' % (self.outputpath, k + 1))
            cmd0 = r'cp %s/tmp%d/megahit_out/final.contigs.fa ./tmp%d.fasta' % (self.outputpath, k, k)
            os.system(cmd0)
            ref_seq = r'tmp%d.fasta' % k
            cmd1 = '%s index -a bwtsw %s' % (self.software_path['bwaPath'],ref_seq)
            os.system(cmd1)
            cmd2 = '%s mem %s %s/%s_1.fq %s/%s_2.fq > %s.sam -t 16' % (self.software_path['bwaPath'],
                ref_seq, self.path_raw, self.seq_name, self.path_raw, self.seq_name, self.seq_name)
            os.system(cmd2)
            cmd3 = 'samtools view -bS -F 4 %s.sam > %s.mapped.bam -@ 16' % (self.seq_name, self.seq_name)
            os.system(cmd3)
            cmd4 = 'samtools sort -o %s.mapped.sorted.bam %s.mapped.bam -@ 1' % (self.seq_name, self.seq_name)
            os.system(cmd4)
            cmd5 = 'samtools index %s.mapped.sorted.bam %s.mapped.sorted.bam.bai' % (self.seq_name, self.seq_name)
            os.system(cmd5)
            cmd6 = '%s bamtofastq -i %s.mapped.sorted.bam -fq %s.mapped.fastq' % (self.software_path['bedtoolsPath'],
                self.seq_name, self.seq_name)
            os.system(cmd6)
            cmd7 = '%s -r %s.mapped.fastq -o megahit_out' % (self.software_path['megahitPath'],self.seq_name)
            os.system(cmd7)
            cmd8 = '%s -in %s -dbtype nucl -out Sdb' % (self.software_path['makeblastdbPath'],ref_seq)
            os.system(cmd8)
            cmd9 = 'cp ./megahit_out/final.contigs.fa ./'
            os.system(cmd9)
            run_path = r'%s/tmp%d' % (self.outputpath, k + 1)
            scountObj = Scount()
            svalue = scountObj.annotation(ref_seq, self.Blast_ident, run_path)
            if svalue >= self.threshold:
                break


if __name__ == '__main__':
    ass = Assemble()
    rst = ass.getConfigContent('params')
    print rst
    ass.runAssemble()
