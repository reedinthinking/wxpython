#!/usr/bin/env python
#encoding:utf-8
import re
import os
from updateConfig.configOpt import ConfigUtil
class Scount(object):
    def __init__(self):
        self.blastn = self.getBlastn()

    def getAbsolutePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print current_dir
        return current_dir

    def getConfigContent(self, key):
        '''return dict :
        '''
        config_path = self.getAbsolutePath() + '/../config/config.ini'
        print "chushi peizhi wenjian*********************"
        print config_path
        myconfig = ConfigUtil(config_path)
        dict = {}
        list = myconfig.get_items(key)
        for item in list:
            dict[item[0]] = item[1]
        return dict

    def getBlastn(self):
        path = self.getConfigContent('software')['blastnPath']
        return path

    def qseqid(self,seq):
        seq_list = seq.split()
        return seq_list[0]

    def sseqid(self,seq):
        seq_list = seq.split()
        return seq_list[1]

    def qstart(self,seq):
        seq_list = seq.split()
        return min(seq_list[6], seq_list[7])

    def qend(self,seq):
        seq_list = seq.split()
        return max(seq_list[6], seq_list[7])

    def sstart(self,seq):
        seq_list = seq.split()
        return min(int(seq_list[8]), int(seq_list[9]))

    def send(self,seq):
        seq_list = seq.split()
        return max(int(seq_list[8]), int(seq_list[9]))

    def qlist(self,alllist):
        list_see_q = []
        for eachline in alllist:
            if self.qseqid(eachline) not in list_see_q:
                list_see_q.append(self.qseqid(eachline))
        return list_see_q

    def slist(self,alllist):
        list_see_s = []
        for eachline in alllist:
            if self.sseqid(eachline) not in list_see_s:
                list_see_s.append(self.sseqid(eachline))
        return list_see_s

    def annotation(self,ref_seq,blast_ident,run_path):
        fr = open('%s/%s'% (run_path,ref_seq),'r')
        lenth_r = 0
        line_cr = fr.readlines()
        for eachline in line_cr:
            if eachline.find('>')!=0:
                lenth_r = lenth_r+len(eachline.strip())
        print lenth_r
        scmd0 = ('%s -query %s/final.contigs.fa -out %s/s_%d_out -db %s/Sdb -outfmt 6  -num_threads 2 -perc_identity %d' %(self.blastn,run_path,run_path,blast_ident, run_path,blast_ident))
        print "---------------------------"
        print scmd0
        os.system(scmd0)
        fr2 = open(r'%s/s_%d_out' %  (run_path,blast_ident), 'r')
        line_cr2 = fr2.readlines()
        sid_list = self.slist(line_cr2)
        a = 0
        s = 0
        for i in sid_list:
            length_mseq = 0
            pos_list = [[0, 0]]
            length_pos_list = []
            for x in range(0,len(line_cr2)):
                print sid_list[a]
                print line_cr2[x]
                if sid_list[a] == self.sseqid(line_cr2[x]):
                    start_seq = self.sstart(line_cr2[x])
                    end_seq = self.send(line_cr2[x])
                    b = 0
                    for i in range(0, len(pos_list)):
                        if (pos_list[i][1] >= start_seq) and (pos_list[i][0] <= end_seq):
                            pos_list[i][0] = min(pos_list[i][0], start_seq)
                            pos_list[i][1] = max(pos_list[i][1], end_seq)
                            break
                    else:
                        pos_list.append([start_seq, end_seq])
            for y in range(0,len(pos_list)):
                for m in range(0,len(pos_list)):
                    if m!=i:
                        if (pos_list[y][1]>=pos_list[m][0]) and (pos_list[y][0] <= pos_list[m][1]):
                            pos_list[y][1]=max(pos_list[y][1],pos_list[m][1])
                            pos_list[y][0] = min(pos_list[y][0], pos_list[m][0])
                            pos_list[m]=[0,0]
            for z in range(0,len(pos_list)):
                length_pos_list.append(pos_list[z][0])
                length_pos_list.append(pos_list[z][1])
                length_mseq = length_mseq + (pos_list[z][1] - pos_list[z][0] + 1)
            coverage = float(length_mseq) / (max(length_pos_list) - min(length_pos_list) + 1)
            a = a + 1
            s = s+(length_mseq/lenth_r)*min(coverage,1/coverage)
        return s

if __name__ == '__main__':
    ass = Scount()
    rst = ass.getBlastn()
    print rst