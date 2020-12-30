#!/usr/bin/env python
#encoding:utf-8
import wx
import os
import sys
import codecs
import subprocess
from updateConfig.configOpt import ConfigUtil
from log import Logger

class SiteLog(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='SiteLog', size=(650, 600))

        #get the current path
        self.abspath = self.getAbsolutePath()
        self.getSoftwarePath()
        self.shell = ''#the subprocess

        #init the log class
        self.log = log = Logger('log/operate.log',level='debug')

        #set the windows
        startx = 5 #the positon of X
        starty = 5 #the positon of Y
        height = 25
        btwidth = 80
        textwidth = 280
        splitwid = 5
        splitheight = 30
        #line 1
        self.SelBtnStatement1 = wx.Button(self, label=u'输入文件', pos=(startx, starty), size=(btwidth, height))#, style = wx.BORDER_NONE
        self.FileName = wx.TextCtrl(self, pos=(startx+btwidth+splitwid, starty), size=(textwidth, height))
        self.SelBtn = wx.Button(self, label='>>', pos=(startx+btwidth+splitwid*7+textwidth, starty), size=(btwidth, height))
        self.SelBtn.Bind(wx.EVT_BUTTON, self.OnOpenFile)
        # self.SelBtn.Bind(wx.EVT_ENTER_WINDOW, self.B)
        # self.SelBtn.Bind(wx.EVT_LEAVE_WINDOW, self.C)
        self.OkBtn2 = wx.Button(self, label=u'查看', pos=(startx+btwidth*2+splitwid*9+textwidth, starty), size=(btwidth, height))
        self.OkBtn2.Bind(wx.EVT_BUTTON, self.ReadFile)

        #line 2
        self.params = {}
        paramwidth = 80
        line2_y = starty+splitheight
        btandtextwidth = btwidth+splitwid*8+paramwidth
        self.SelBtnStatement2 = wx.Button(self, label=u'线程数', pos=(startx, line2_y), size=(btwidth, height))
        self.theadnum = wx.TextCtrl(self, value="16",pos=(startx+btwidth+splitwid, line2_y), size=(paramwidth, height))
        self.SelBtnStatement2.Bind(wx.EVT_BUTTON, self.setParams)
        #print self.theadnum.GetValue()
        self.SelBtnStatement22 = wx.Button(self, label=u'阈值', pos=(startx+btandtextwidth, starty + splitheight),
                                          size=(btwidth, height))
        self.threshold = wx.TextCtrl(self, value="0.99",pos=(startx+btandtextwidth+btwidth+splitwid, line2_y),
                                    size=(paramwidth, height))
        self.SelBtnStatement22.Bind(wx.EVT_BUTTON, self.setParams)
        self.SelBtnStatement23 = wx.Button(self, label=u'Blast_ident',
                                           pos=(startx+btandtextwidth*2, line2_y),
                                           size=(btwidth, height))
        self.blast_ident = wx.TextCtrl(self, value="85",pos=(startx+btandtextwidth*2+btwidth+splitwid, line2_y),
                                     size=(paramwidth, height))
        self.SelBtnStatement23.Bind(wx.EVT_BUTTON, self.setParams)


        #line 3
        line3_y = starty+splitheight*2
        self.SelBtnStatement3 = wx.Button(self, label=u'输出路径', pos=(startx, line3_y), size=(btwidth, height))
        self.FileDir = wx.TextCtrl(self, pos=(startx+btwidth+splitwid, line3_y), size=(280, 25))  # label='输出路径',
        self.SelBtn3 = wx.Button(self, label='>>', pos=(startx+btwidth+splitwid*7+textwidth, line3_y), size=(btwidth, height))
        self.SelBtn3.Bind(wx.EVT_BUTTON, self.OnOpenFileDir)
        self.SelBtn32 = wx.Button(self, label='Start',pos=(startx+btwidth*2+splitwid*9+textwidth, line3_y),size=(btwidth, height))
        self.SelBtn32.Bind(wx.EVT_BUTTON, self.runAnalysis)

        self.FileContent = wx.TextCtrl(self, pos=(startx, starty+splitheight*3), size=(620, 480), style=(wx.TE_MULTILINE))

    def B(self,evt):
        wx.Frame.SetBackgroundColour("#FFFFFF")

    def C(self,evt):
        wx.Frame.SetBackgroundColour("#EFEFEF")

    def OnOpenFile(self, event):#文件选择
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.FileName.SetValue(dialog.GetPath())
            logstr = "选择待分析文件：" + dialog.GetPath()
            self.log.logger.info(logstr)
            dictfilepath = {'filepath': {'inputfile': dialog.GetPath()}}
            try:
                self.updateConfig(dictfilepath)
                logstr = "成功更新配置文件：inputfile"
                self.log.logger.info(logstr)
            except Exception as error:
                logstr = "更新配置文件：inputfile"
                self.log.logger.error(logstr)


            dialog.Destroy

    def OnOpenFileDir(self, event):#文件夹选择
        """"""
        dialog = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()  # 文件夹路径
            self.FileDir.SetValue(dialog.GetPath())
            dictfilepath = {'filepath':{'outputpath':dialog.GetPath()}}
            self.updateConfig(dictfilepath)
        dialog.Destroy()

    def ReadFile(self, event):
        print self.FileName.GetValue()
        with codecs.open(self.FileName.GetValue(),'a+','utf-8') as file:
            #file = open(self.FileName.GetValue(),'a',encoding='utf-8')
            self.FileContent.SetValue(file.read())
            file.close()

    def setParams(self,event):
        self.params['threadnum'] = self.theadnum.GetValue()
        self.params['threshold'] = self.threshold.GetValue()
        self.params['Blast_ident'] = self.blast_ident.GetValue()
        self.updateConfig({'params':self.params})

        #self.FileContent.SetValue(event.GetString())

    def updateConfig(self, params):
        config_path = self.abspath + '/config/config.ini'
        myconfig = ConfigUtil(config_path)
        myconfig.update_config(params)

    def getAbsolutePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print current_dir
        return current_dir

    def getSoftwarePath(self):
        '''return dict :
        '''
        config_path = self.abspath + '/config/config.ini'
        # print "chushi peizhi wenjian*********************"
        # print config_path
        myconfig = ConfigUtil(config_path)
        dict = {}
        list = myconfig.get_items('software')
        for item in list:
            dict[item[0]] = item[1]
        return dict

    def check_output(*popenargs, **kwargs):#
        process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output
        #p = subprocess.check_output('ifconfig')

    def runAnalysis(self,event):
        #redir = RedirectText(self.FileContent)
        btnLabel = self.SelBtn32.GetLabel()
        print btnLabel

        font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')


        if btnLabel == "Start":

            os_str = '/home/ubuntu/anaconda2/bin/python ' + self.abspath + '/analysisFile/assemble.py'  # D:\\anaconda\\
            print os_str
            #os_str = "ipconfig"
            #self.check = subprocess.check_call(os_str)
            #print self.check
            self.shell = subprocess.Popen(os_str, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                 universal_newlines=True)
            # subprocess.STDOUT = redir
            # sys.stderr = redir
            outstr = ''
            self.SelBtn32.SetLabel("Stop")
            self.FileContent.Clear()
            while True:
                nextline = self.shell.stdout.readline()
                outstr += nextline  # + '\r\n'
                #print(nextline.strip())
                # self.FileContent.Clear()
                self.FileContent.AppendText(nextline)
                wx.Yield()
                if nextline == "" and self.shell.poll() != None:
                    break
                #print outstr
                # self.FileContent.SetValue(outstr)
            nexterrline = self.shell.stderr.readline()
            print '----------------------------'
            print nexterrline
            #self.FileContent.SetFont(font1)
            while True:
                nexterrline = self.shell.stderr.readline()
                outstr += nexterrline  # + '\r\n'
                print(nexterrline.strip())
                # self.FileContent.Clear()
                if 'OSError' in nexterrline:
                    self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
                elif 'mkdir' in nexterrline:
                    self.FileContent.SetDefaultStyle(wx.TextAttr("BLUE"))
                else:
                    self.FileContent.SetDefaultStyle(wx.TextAttr("BLACK"))
                self.FileContent.AppendText(nexterrline)
                wx.Yield()
                if nexterrline == "" and self.shell.poll() != None:
                    break
                #print outstr
        else:
            self.shell.kill()
            self.SelBtn32.SetLabel("Start")



# class RedirectText(object):
#     def __init__(self,aWxTextCtrl):
#      self.out=aWxTextCtrl
#
#     def write(self,string):
#      self.out.WriteText(string)

if __name__ == '__main__':
    app = wx.App(redirect=False)
    SiteFrame = SiteLog()
    #my_panel = MyPanel(SiteFrame, -1)
    SiteFrame.Show()

    # frame = wx.Frame(None, -1, '登陆窗口', size=(300, 200))
    # my_panel = MyPanel(frame, -1)
    app.MainLoop()