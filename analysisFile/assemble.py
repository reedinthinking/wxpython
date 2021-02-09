#!/usr/bin/env python
# encoding:utf-8
import re
import os
from analysisFile.Scount import Scount
from updateConfig.configOpt import ConfigUtil
from log import Logger
import datetime
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator


class Assemble(object):

    def __init__(self):
        self.abspath = self.getAbsolutePath()
        self.filepath = self.getConfigContent('filepath')
        self.path_raw = self.filepath['inputfile'][:(self.filepath['inputfile'].rfind('/') )]
        self.ref = self.filepath['inputfile'][(self.filepath['inputfile'].rfind('/') + 1):]
        self.outputpath = self.filepath['outputpath']

        self.params = self.getConfigContent('params')
        self.seq_name = self.params['seq_name']
        self.max_run = int(self.params['max_run'])
        self.Blast_ident = int(self.params['Blast_ident'])
        self.threshold = float(self.params['threshold'])
        self.threadnum = int(self.params['threadnum'])

        self.software_path = self.getConfigContent('software')

        # init the log class
        #self.logLevel = self.getConfigContent('config')['logLevel']
        self.log = self.getLogger()#Logger(self.abspath + '/../log/operate.log', level=self.logLevel)

    def getLogger(self):
        logLevel = self.getConfigContent('config')['logLevel']
        logfile = self.abspath + '/../log/operate-'+datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        log = Logger(logfile, level=logLevel)
        return log

    def getAbsolutePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #print current_dir
        return current_dir

    def getConfigContent(self, key):
        '''return dict :
        '''
        config_path = self.abspath + '/../config/config.ini'
        # print "chushi peizhi wenjian*********************"
        # print config_path
        myconfig = ConfigUtil(config_path)
        dict = {}
        list = myconfig.get_items(key)
        for item in list:
            dict[item[0]] = item[1]
        return dict

    def drawPicture(self,datafile, savefile):
        logstr = "start to draw the picture--the data file：%s;the output picture file:%s" % (datafile,savefile)
        self.log.logger.info(logstr)
        print logstr
        rs = os.path.exists(datafile)
        x = []
        y = []
        i=0
        if rs == True:
            print 1
            file_handler = open(datafile, mode='r')
            contents = file_handler.readlines()
            for msg in contents:
                i += 1
                msg = msg.strip(' ')
                msg = msg.strip('\n')
                #print msg
                list_1 = msg.split('\t')
                if i<=101:
                    if len(list_1) == 3:
                        x.append(list_1[1])
                        y.append(list_1[2])
        else:
            logstr = "the data file：%s is not found" % (datafile)
            self.log.logger.info(logstr)
            print logstr
        plt.plot(x, y, linewidth=2)

        plt.xlabel('Numbers', fontsize=9)
        plt.ylabel('Squares', fontsize=9)
        x_major_locator = MultipleLocator(50)
        # 把x轴的刻度间隔设置为1，并存在变量里
        y_major_locator = MultipleLocator(100)
        # 把y轴的刻度间隔设置为10，并存在变量里

        ax = plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        # 把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)

        plt.xlim(-1, 200)
        # 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
        plt.ylim(-1, 500)
        # 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白

        # 保存图片到本地
        plt.savefig(savefile)
        # 显示图片
        #plt.show()

    def check_output(self,popenargs):  # 检查执行命令是否出错
        # s = subprocess.Popen(popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                      universal_newlines=True)
        # # output, unused_err = s.communicate()
        # # print unused_err
        # while True:
        #     nextline = s.stderr.readline()
        #     # outstr += nextline #+ '\r\n'
        #     print(nextline.strip())
        #     if nextline == "" or s.poll() != None:
        #         break
        #os.system(popenargs)
        p = subprocess.Popen(popenargs, stdout=subprocess.PIPE, shell=True,
                             stderr=subprocess.PIPE)  # , close_fds=True)

        out, err = p.communicate()
        if p.returncode != 0:
            print err
        self.log.logger.info(p.stdout)

    #p = check_output(os_str)

    def runAssemble(self):
        outfile = ''#> /dev/null
        self.curr_time = datetime.datetime.now()
        logstr = "*程序开始运行时间：%s"  % self.curr_time.strftime("%Y-%m-%d %H:%M:%S")
        self.log.logger.info(logstr)
        print logstr
        try:
            os.mkdir(r'%s/tmp0' % self.outputpath)
            os.mkdir(r'%s/tmp0/megahit_out' % self.outputpath)
            logstr = "*成功创建临时目标文件夹：" + (r'%s/tmp0' % self.outputpath)
            self.log.logger.info(logstr)
            print logstr
        except Exception as error:
            logstr = "*创建临时目标文件夹失败："+ (r'%s/tmp0' % self.outputpath)
            self.log.logger.error(logstr)
            self.log.logger.error(error)
            print logstr
            print error

        cmd00 = r'cp %s/%s %s/tmp0/megahit_out/final.contigs.fa' % (self.path_raw, self.ref, self.outputpath)
        os.system(cmd00)
        logstr = "*复制待分析文件到临时目标文件夹：%s" % (cmd00)
        self.log.logger.info(logstr)
        print logstr
        for k in range(0, self.max_run):
            logstr = r'*开始第%d次循环------------' % (k+1)
            self.log.logger.info(logstr)
            print logstr
            try:
                os.mkdir(r'%s/tmp%d' % (self.outputpath, k + 1))
                os.chdir(r'%s/tmp%d' % (self.outputpath, k + 1))
                current_path = r'%s/tmp%d' % (self.outputpath, k + 1)
                logstr = "*循环%d：迭代开始--10.1：建立文件夹tmp_k：%s/tmp%d"  % ( k+1,self.outputpath,k+1)
                self.log.logger.info(logstr)
                print logstr
            except Exception as error:
                logstr = "*循环%d：迭代开始--10.1：建立文件夹tmp_k失败：%s/tmp%d"  % ( k+1,self.outputpath,k+1)
                self.log.logger.error(logstr)
                self.log.logger.error(error)
                print logstr
                print error

            cmd0 = r'cp %s/tmp%d/megahit_out/final.contigs.fa ./tmp%d.fasta' % (self.outputpath, k, k)
            os.system(cmd0)
            logstr = "*循环%d：迭代开始--10.2：复制第k-1次MEGAHIT输出文件final.contigs.fa至tmp_k，并将final.contigs.fa修改文件名为ref_k-1.fasta--%s" % (k+1, cmd0)
            self.log.logger.info(logstr)
            print logstr

            ref_seq = r'tmp%d.fasta' % k
            cmd1 = '%s index -a bwtsw %s %s' % (self.software_path['bwaPath'],ref_seq,outfile)
            self.check_output(cmd1)
            logstr = "*循环%d：Step1：调用bwa对ref.fasta建立比对索引--%s" % (k+1, cmd1)
            self.log.logger.info(logstr)
            print logstr

            cmd2 = '%s mem %s %s %s > %s.sam -t 16 %s' % (
            self.software_path['bwaPath'], ref_seq, self.filepath['seqfile1'], self.filepath['seqfile2'], self.seq_name,
            outfile)
            self.check_output(cmd2)
            logstr = "*循环%d：Step2：调用bwa的比对功能bwa mem--%s" % (k + 1, cmd2)
            self.log.logger.info(logstr)
            print logstr

            cmd3 = 'samtools view -bS -F 4 %s.sam > %s.mapped.bam -@ %d %s' % (self.seq_name, self.seq_name,self.threadnum,outfile)
            self.check_output(cmd3)
            logstr = "*循环%d：Step3：调用samtools 的view功能，提取比对到ref.fasta的比对结果，生成bam格式的文件--%s" % (k + 1, cmd3)
            self.log.logger.info(logstr)
            print logstr

            cmd4 = 'samtools sort -o %s.mapped.sorted.bam %s.mapped.bam -@ 1 %s' % (self.seq_name, self.seq_name,outfile)
            self.check_output(cmd4)
            logstr = "*循环%d：Step4：调用samtools的sort功能，对bam格式的比对结果进行重排序--%s" % (k + 1, cmd4)
            self.log.logger.info(logstr)
            print logstr

            cmd5 = 'samtools index %s.mapped.sorted.bam %s.mapped.sorted.bam.bai %s' % (self.seq_name, self.seq_name,outfile)
            self.check_output(cmd5)
            logstr = "*循环%d：Step5：调用samtools的index功能，对重排序的比对结果建立索引--%s" % (k + 1, cmd5)
            self.log.logger.info(logstr)
            print logstr

            cmd6 = '%s bamtofastq -i %s.mapped.sorted.bam -fq %s.mapped.fastq %s' % (self.software_path['bedtoolsPath'],
                self.seq_name, self.seq_name,outfile)
            self.check_output(cmd6)
            logstr = "*循环%d：Step6：调用bedtools的bamtofastq功能，将重排序的比对结果转化为fastq格式的序列--%s" % (k + 1, cmd6)
            self.log.logger.info(logstr)
            print logstr

            cmd7 = '%s -r %s.mapped.fastq -o megahit_out %s' % (self.software_path['megahitPath'],self.seq_name,outfile)
            self.check_output(cmd7)
            logstr = "*循环%d：Step7：调用MEGAHIT进行序列组装--%s" % (k + 1, cmd7)
            self.log.logger.info(logstr)
            print logstr

            cmd8 = '%s -in %s -dbtype nucl -out Sdb %s' % (self.software_path['makeblastdbPath'],ref_seq,outfile)
            self.check_output(cmd8)
            logstr = "*循环%d：Step8：调用BLAST的makeblastdb模块对final.contigs.fa建立索引，使用blastn模块根据设定参数对ref.fasta进行同源性比对--%s" % (k + 1, cmd8)
            self.log.logger.info(logstr)
            print logstr

            cmd9 = 'cp ./megahit_out/final.contigs.fa ./'
            self.check_output(cmd9)
            logstr = "*循环%d：Step9：使用个人编写的python脚本对Step8的比对结果进行解析，计算同源性S0--%s" % (k + 1, cmd9)
            self.log.logger.info(logstr)
            print logstr

            cmd10 = 'samtools depth -a %s.mapped.sorted.bam > depth.txt' % self.seq_name
            self.check_output(cmd10)
            logstr = "*循环%d：Step10(new add)：每个tmp文件夹中会生成一个depth.txt文档，该文档的第二列作为横坐标，第三列作为纵坐标--%s" % (k + 1, cmd10)
            self.log.logger.info(logstr)
            print logstr

            #draw the picture of the output data
            datafile = current_path + '/depth.txt'
            savefile = current_path + '/output.png'
            self.drawPicture(datafile,savefile)


            logstr = "*循环%d：Step10：调用Scout计算阈值cutoff值Sn" % (k + 1)
            self.log.logger.info(logstr)
            print logstr

            run_path = r'%s/tmp%d' % (self.outputpath, k + 1)
            scountObj = Scount()
            svalue = scountObj.annotation(ref_seq, self.Blast_ident, run_path)
            if svalue >= self.threshold:
                logstr = "*循环%d：Step10：迭代组装，迭代终止cutoff值Sn设置为99%" % (k + 1)
                self.log.logger.info(logstr)
                print logstr
                break
        self.curr_time2 = datetime.datetime.now()
        logstr = "*程序运行结束时间：%s" % self.curr_time.strftime("%Y-%m-%d %H:%M:%S")
        self.log.logger.info(logstr)
        print logstr

        minutes = int((self.curr_time2-self.curr_time).total_seconds() / 60)
        seconds = int((self.curr_time2 - self.curr_time).total_seconds() / 60)
        logstr = "*程序运行时间：%d分%d秒" % (minutes,seconds)
        self.log.logger.info(logstr)
        print logstr

if __name__ == '__main__':
    ass = Assemble()
    rst = ass.getConfigContent('params')
    print rst
    ass.runAssemble()
