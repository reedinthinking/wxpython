#!/usr/bin/env python
# encoding:utf-8
import wx
import os
import signal
import sys
import codecs
import subprocess
import re
from updateConfig.configOpt import ConfigUtil
from log import Logger
import datetime


class SiteLog(wx.Frame):
    def __init__(self, parent, title):
        super(SiteLog, self).__init__(parent, title=title, size=(900, 800))
        #self.Bind(wx.EVT_CLOSE, self.showWindow)
        self.InitUI()
        self.Centre()

        # get the current path
        self.params = {}
        self.abspath = self.getAbsolutePath()
        self.shell = ''  # the subprocess
        # init the log class
        # self.logLevel = self.getConfig('config')['logLevel']
        self.log = self.getLogger()#Logger('log/operate.log', level=self.logLevel)

    # def showWindow(self,evt):
    #     frame = self.GetParent()
    #     print frame
    #     frame.show()

    def InitUI(self):

        # panel = wx.Panel(self)
        panel = TabPanel(self, -1)

        # 水平盒子
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        # font.SetPointSize(9)

        fonttitle = wx.Font(16, 70, 90, 90, False, "宋体")
        fonttitle.SetPointSize(14)
        fonttitle2 = wx.Font(16, 70, 90, 90, False, "宋体")
        fonttitle2.SetPointSize(10)

        textfont = wx.Font(11, 74, 90, 92, False, "Microsoft Sans Serif")
        textfont.SetPointSize(10)

        ctrfont = wx.Font(11, 74, 90, 92, False, "Microsoft Sans Serif")
        ctrfont.SetPointSize(10)

        # sb1 = wx.StaticBox(panel, label="Param set")
        sizer = wx.GridBagSizer(8, 5)
        sizer.SetMinSize(wx.Size(300, 480))
        sizerborder = 5

        bmp = wx.Image("image/open.bmp", wx.BITMAP_TYPE_ANY)  # .ConvertToBitmap()
        w = bmp.GetWidth()
        h = bmp.GetHeight()
        print w
        print h
        bmp = bmp.Scale(w / 3, h / 3)
        bmp = bmp.ConvertToBitmap()

        bmp2 = wx.Image("image/open1.bmp", wx.BITMAP_TYPE_BMP)  # .ConvertToBitmap()
        w = bmp2.GetWidth()
        h = bmp2.GetHeight()
        print w
        print h
        bmp2 = bmp2.Scale(w / 3, h / 3)
        bmp2 = bmp2.ConvertToBitmap()

        text = wx.StaticText(panel, label=u"Iterative assembly")
        text.SetFont(fonttitle)
        text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        sizer.Add(text, pos=(0, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=sizerborder)
        # icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('image/exec.png'))
        # sizer.Add(icon, pos=(0, 4), flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT,
        #           border=sizerborder)
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.BOTTOM, border=sizerborder)

        text1 = wx.StaticText(panel, label=u'add(ref)')
        text1.SetFont(textfont)
        text1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        sizer.Add(text1, pos=(2, 0), flag=wx.LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.tc1 = wx.TextCtrl(panel)
        self.tc1.SetFont(textfont)
        self.tc1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        sizer.Add(self.tc1, pos=(2, 1), span=(1, 3), flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=sizerborder)
        button1 = wx.BitmapButton(panel, -1, bmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        button1.SetBitmapFocus(bmp2)
        button1.Bind(wx.EVT_BUTTON, self.OnOpenFile1)
        sizer.Add(button1, pos=(2, 4), flag=wx.RIGHT | wx.ALL, border=sizerborder)

        text2 = wx.StaticText(panel, label="add(seq-1)")
        text2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        text2.SetFont(textfont)
        sizer.Add(text2, pos=(3, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.tc2 = wx.TextCtrl(panel)
        self.tc2.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.tc2.SetFont(textfont)
        sizer.Add(self.tc2, pos=(3, 1), span=(1, 3), flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=sizerborder)
        button2 = wx.BitmapButton(panel, -1, bmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        button2.SetBitmapFocus(bmp2)
        button2.Bind(wx.EVT_BUTTON, self.OnOpenFile2)
        sizer.Add(button2, pos=(3, 4), flag=wx.CENTER | wx.RIGHT | wx.ALL, border=sizerborder)

        text3 = wx.StaticText(panel, label="add(seq-2)")
        text3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        text3.SetFont(textfont)
        sizer.Add(text3, pos=(4, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.tc3 = wx.TextCtrl(panel)
        self.tc3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.tc3.SetFont(textfont)
        sizer.Add(self.tc3, pos=(4, 1), span=(1, 3), flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=sizerborder)
        button3 = wx.BitmapButton(panel, -1, bmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        button3.SetBitmapFocus(bmp2)
        button3.Bind(wx.EVT_BUTTON, self.OnOpenFile3)
        sizer.Add(button3, pos=(4, 4), flag=wx.CENTER | wx.RIGHT | wx.ALL, border=sizerborder)

        text4 = wx.StaticText(panel, label="output")
        text4.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        text4.SetFont(textfont)
        sizer.Add(text4, pos=(5, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.tc4 = wx.TextCtrl(panel)
        self.tc4.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.tc4.SetFont(textfont)
        sizer.Add(self.tc4, pos=(5, 1), span=(1, 3), flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, border=sizerborder)
        button4 = wx.BitmapButton(panel, -1, bmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        button4.SetBitmapFocus(bmp2)
        button4.Bind(wx.EVT_BUTTON, self.OnOpenFileDir)
        sizer.Add(button4, pos=(5, 4), flag=wx.CENTER | wx.RIGHT | wx.ALL, border=sizerborder)

        # text5 = wx.StaticText(panel, label="")
        # sizer.Add(text5, pos=(6, 0), span=(1, 1), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        sizer.AddGrowableCol(2)

        # 参数设置
        sb = wx.StaticBox(panel, label="Param set")
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        paramsizer = wx.GridBagSizer(5, 5)
        sizer.SetMinSize(wx.Size(200, 200))

        paramtext = wx.StaticText(panel, label="thread")
        paramtext.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        paramtext.SetFont(textfont)
        paramsizer.Add(paramtext, pos=(0, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.theadnum = wx.TextCtrl(panel, value="16")
        self.theadnum.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.theadnum.SetFont(textfont)
        paramsizer.Add(self.theadnum, pos=(0, 3), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)

        paramtext2 = wx.StaticText(panel, label="threshold")
        paramtext2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        paramtext2.SetFont(textfont)
        paramsizer.Add(paramtext2, pos=(1, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.threshold = wx.TextCtrl(panel, value="0.99")
        self.threshold.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.threshold.SetFont(textfont)
        paramsizer.Add(self.threshold, pos=(1, 3), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)

        # set the update button
        parambmp = wx.Image("image/update.bmp", wx.BITMAP_TYPE_ANY)  # .ConvertToBitmap()
        w = parambmp.GetWidth()
        h = parambmp.GetHeight()
        print w
        print h
        parambmp = parambmp.Scale(w / 3, h / 3)
        parambmp = parambmp.ConvertToBitmap()

        parambmp2 = wx.Image("image/update1.bmp", wx.BITMAP_TYPE_BMP)  # .ConvertToBitmap()
        w = parambmp2.GetWidth()
        h = parambmp2.GetHeight()
        print w
        print h
        parambmp2 = parambmp2.Scale(w / 3, h / 3)
        parambmp2 = parambmp2.ConvertToBitmap()
        updatebtn = wx.BitmapButton(panel, -1, parambmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        updatebtn.SetBitmapFocus(parambmp2)
        updatebtn.Bind(wx.EVT_BUTTON, self.setParams)
        # text6 = wx.StaticText(panel, label="")
        # paramsizer.Add(text6, pos=(1, 4), flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,border=sizerborder)
        paramsizer.Add(updatebtn, pos=(1, 4), flag=wx.LEFT | wx.ALL, border=sizerborder)

        paramtext3 = wx.StaticText(panel, label="Blast_ident")
        paramtext3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        paramtext3.SetFont(textfont)
        paramsizer.Add(paramtext3, pos=(2, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        self.Blast_ident = wx.TextCtrl(panel, value="85")
        self.Blast_ident.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.Blast_ident.SetFont(textfont)
        paramsizer.Add(self.Blast_ident, pos=(2, 3), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=sizerborder)
        paramsizer.AddGrowableCol(2)

        boxsizer.Add(paramsizer)

        sizer.Add(boxsizer, pos=(6, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        line2 = wx.StaticLine(panel)
        sizer.Add(line2, pos=(7, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.BOTTOM, border=sizerborder)

        # set the start button
        startbmp = wx.Image("image/start.jpg", wx.BITMAP_TYPE_ANY)  # .ConvertToBitmap()
        w = startbmp.GetWidth()
        h = startbmp.GetHeight()
        print w
        print h
        startbmp = startbmp.Scale(w / 4, h / 4)
        startbmp = startbmp.ConvertToBitmap()

        startbmp2 = wx.Image("image/start1.jpg", wx.BITMAP_TYPE_ANY)  # .ConvertToBitmap()
        w = startbmp2.GetWidth()
        h = startbmp2.GetHeight()
        print w
        print h
        startbmp2 = startbmp2.Scale(w / 4, h / 4)
        startbmp2 = startbmp2.ConvertToBitmap()
        startbtn = wx.BitmapButton(panel, -1, startbmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        startbtn.SetBitmapFocus(startbmp2)
        startbtn.Bind(wx.EVT_BUTTON, self.runAnalysis)
        # text6 = wx.StaticText(panel, label="")
        # paramsizer.Add(text6, pos=(1, 4), flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,border=sizerborder)
        sizer.Add(startbtn, pos=(8, 2), flag=wx.CENTER | wx.RIGHT | wx.ALL, border=sizerborder)

        # # set the stop button
        # stopbmp = wx.Image("image/stop.jpg", wx.BITMAP_TYPE_ANY)  # .ConvertToBitmap()
        # w = stopbmp.GetWidth()
        # h = stopbmp.GetHeight()
        # print w
        # print h
        # stopbmp = stopbmp.Scale(w / 4, h / 4)
        # stopbmp = stopbmp.ConvertToBitmap()
        #
        # stopbmp2 = wx.Image("image/stop1.jpg", wx.BITMAP_TYPE_ANY)  # .ConvertToBitmap()
        # w = stopbmp2.GetWidth()
        # h = stopbmp2.GetHeight()
        # print w
        # print h
        # stopbmp2 = stopbmp2.Scale(w / 4, h / 4)
        # stopbmp2 = stopbmp2.ConvertToBitmap()
        # stopbtn = wx.BitmapButton(panel, -1, stopbmp, size=wx.DefaultSize, style=wx.BORDER_NONE)
        # stopbtn.SetBitmapFocus(stopbmp2)
        # stopbtn.Bind(wx.EVT_BUTTON, self.stopAnalysis)
        # # text6 = wx.StaticText(panel, label="")
        # # paramsizer.Add(text6, pos=(1, 4), flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,border=sizerborder)
        # sizer.Add(stopbtn, pos=(8, 3), flag=wx.CENTER | wx.RIGHT | wx.ALL, border=sizerborder)

        hbox.Add(sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=20)

        hbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.VERTICAL)

        text7 = wx.StaticText(panel, label=u"Run Log")
        text7.SetFont(fonttitle2)
        text7.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        hbox3.Add(text7, 0, flag=wx.CENTER | wx.ALL, border=20)

        # line3 = wx.StaticLine(panel)
        # hbox3.Add(line3, flag=wx.EXPAND | wx.BOTTOM, border=sizerborder)

        self.FileContent = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(450, 150))
        hbox3.Add(self.FileContent, proportion=1, flag=wx.EXPAND)
        hbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=20)

        hbox.Add((-1, 25))

        panel.SetSizer(hbox)

        panel.SetSizer(hbox)
        hbox.Fit(self)
        # panel.GetSizer().Fit(self)
        panel.Centre(wx.BOTH)
    def getLogger(self):
        logLevel = self.getConfig('config')['logLevel']
        logfile = self.abspath + '/log/operate-'+datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        log = Logger(logfile, level=logLevel)
        return log


    def B(self, evt):
        wx.Frame.SetBackgroundColour("#FFFFFF")

    def C(self, evt):
        wx.Frame.SetBackgroundColour("#EFEFEF")

    def OnOpenFile1(self, event):  # 文件选择
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.tc1.SetValue(dialog.GetPath())
            logstr = "选择待分析文件：" + dialog.GetPath()
            self.log.logger.info(logstr)
            dictfilepath = {'filepath': {'inputfile': dialog.GetPath()}}
            try:
                self.updateConfig(dictfilepath)
                logstr = "成功更新配置文件：inputfile"
                self.log.logger.info(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
            except Exception as error:
                logstr = "更新配置文件失败：inputfile"
                self.log.logger.error(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
                self.log.logger.error(error)
            dialog.Destroy

    def OnOpenFile2(self, event):  # 文件选择
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.tc2.SetValue(dialog.GetPath())
            logstr = "选择待分析文件：" + dialog.GetPath()
            self.log.logger.info(logstr)
            dictfilepath = {'filepath': {'seqfile1': dialog.GetPath()}}
            try:
                self.updateConfig(dictfilepath)
                logstr = "成功更新配置文件：seqfile1"
                self.log.logger.info(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
            except Exception as error:
                logstr = "更新配置文件失败：seqfile1"
                self.log.logger.error(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
                self.log.logger.error(error)
            dialog.Destroy

    def OnOpenFile3(self, event):  # 文件选择
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.tc3.SetValue(dialog.GetPath())
            logstr = "选择待分析文件：" + dialog.GetPath()
            self.log.logger.info(logstr)
            dictfilepath = {'filepath': {'seqfile2': dialog.GetPath()}}
            try:
                self.updateConfig(dictfilepath)
                logstr = "成功更新配置文件：seqfile2"
                self.log.logger.info(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
            except Exception as error:
                logstr = "更新配置文件失败：seqfile2"
                self.log.logger.error(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
                self.log.logger.error(error)
            dialog.Destroy


    def OnOpenFileDir(self, event):  # 文件夹选择
        """"""
        dialog = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            print dialog.GetPath()  # 文件夹路径
            self.tc4.SetValue(dialog.GetPath())

            logstr = "选择输出文件夹：" + dialog.GetPath()
            self.log.logger.info(logstr)
            dictfilepath = {'filepath': {'outputpath': dialog.GetPath()}}
            try:
                self.updateConfig(dictfilepath)
                logstr = "成功更新配置文件：outputpath"
                self.log.logger.info(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
            except Exception as error:
                logstr = "更新配置文件失败：outputpath"
                self.log.logger.error(logstr)
                self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
                self.FileContent.AppendText(logstr)
                self.FileContent.AppendText("\r\n")
                self.log.logger.error(error)

        dialog.Destroy()

    def ReadFile(self, event):
        #print self.FileName.GetValue()
        with codecs.open(self.FileName.GetValue(), 'a+', 'utf-8') as file:
            # file = open(self.FileName.GetValue(),'a',encoding='utf-8')
            logstr = "查看选择的文件内容"
            self.log.logger.info(logstr)
            #self.FileContent.Clear()
            self.FileContent.SetDefaultStyle(wx.TextAttr("BLACK"))
            self.FileContent.SetValue(file.read())
            file.close()

    def setParams(self, event):
        self.params['threadnum'] = self.theadnum.GetValue()
        self.params['threshold'] = self.threshold.GetValue()
        self.params['Blast_ident'] = self.blast_ident.GetValue()
        try:
            self.updateConfig({'params': self.params})
            logstr = "成功更新配置文件：threadnum、threshold、Blast_ident"
            self.log.logger.info(logstr)
            self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
            self.FileContent.AppendText(logstr)
            self.FileContent.AppendText("\r\n")
        except Exception as error:
            logstr = "更新配置文件失败：：threadnum、threshold、Blast_ident"
            self.log.logger.error(logstr)
            self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
            self.FileContent.AppendText(logstr)
            self.FileContent.AppendText("\r\n")
            self.log.logger.error(error)

        # self.FileContent.SetValue(event.GetString())

    def updateConfig(self, params):
        config_path = self.abspath + '/config/config.ini'
        myconfig = ConfigUtil(config_path)
        myconfig.update_config(params)

    def getAbsolutePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logstr = "获取当前执行文件路径：" + current_dir
        self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
        self.FileContent.AppendText(logstr)
        self.FileContent.AppendText("\r\n")
        #self.log.logger.debug(logstr)
        #print current_dir
        return current_dir

    def getConfig(self,param):
        '''return dict :
        '''
        config_path = self.abspath + '/config/config.ini'
        # print "chushi peizhi wenjian*********************"
        # print config_path

        myconfig = ConfigUtil(config_path)
        dict = {}
        try:
            list = myconfig.get_items(param)
            for item in list:
                dict[item[0]] = item[1]
            logstr = "成功读取配置文件："+param
            self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
            self.FileContent.AppendText(logstr)
            self.FileContent.AppendText("\r\n")
            #self.log.logger.debug(logstr)
        except Exception as error:
            logstr = "读取配置文件失败："+param
            self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
            self.FileContent.AppendText(logstr)
            self.FileContent.AppendText("\r\n")
            #self.log.logger.error(logstr)
            #self.log.logger.error(error)

        return dict

    def check_output(*popenargs, **kwargs):  #检查执行命令是否出错
        process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output
        # p = subprocess.check_output('ifconfig')

    def runAnalysisbak(self, event):
        # redir = RedirectText(self.FileContent)
        btnLabel = self.SelBtn32.GetLabel()
        print btnLabel
        # #设置文本框不同行信息的字体格式
        # if 'OSError' in nexterrline:
        #     self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
        # elif 'mkdir' in nexterrline:
        #     self.FileContent.SetDefaultStyle(wx.TextAttr("BLUE"))
        # else:
        #     self.FileContent.SetDefaultStyle(wx.TextAttr("BLACK"))
        # self.FileContent.AppendText(nexterrline)
        if btnLabel == "Start":

            os_str = '/home/ubuntu/anaconda2/bin/python ' + self.abspath + '/analysisFile/assemble.py'  # D:\\anaconda\\
            logstr = "调用程序指令：" + os_str
            self.log.logger.debug(logstr)

            # os_str = "ipconfig"
            # self.check = subprocess.check_call(os_str)
            # print self.check
            self.shell = subprocess.Popen(os_str, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                          universal_newlines=True)
            self.SelBtn32.SetLabel("Stop")
            self.FileContent.Clear()

            logstr = "开始运行分析程序……"
            self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
            self.FileContent.AppendText(logstr)
            self.FileContent.AppendText("\r\n")

            regex1 = "\^*"#输出匹配，只在界面显示**开头的关键信息
            regex2 = "\^*程序"  # 输出匹配，只在界面显示**开头的关键信息
            while True:
                nextline = self.shell.stdout.readline()
                if nextline == "" and self.shell.poll() != None:
                    break
                # print(nextline.strip())
                # self.FileContent.Clear()
                if re.search(regex1, nextline):
                    if re.search(regex2, nextline):
                        self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
                    else:
                        self.FileContent.SetDefaultStyle(wx.TextAttr("BLACK"))
                    self.FileContent.AppendText(nextline)
                    wx.Yield()
                    logstr = "正在分析……：" + nextline
                    self.log.logger.info(logstr)
                else:
                    logstr = "正在分析……：" + nextline
                    self.log.logger.debug(logstr)

                    # print outstr
                    # self.FileContent.SetValue(outstr)
            nexterrline = self.shell.stderr.readline()
            logstr = "程序出错……：" + nexterrline
            self.log.logger.error(logstr)
            if nexterrline != "":
                self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
                self.FileContent.AppendText(nexterrline)
                self.SelBtn32.SetLabel("Start")
            while True:
                nexterrline = self.shell.stderr.readline()
                #print(nexterrline.strip())
                # self.FileContent.Clear()
                self.FileContent.AppendText(nexterrline)
                wx.Yield()
                logstr = "程序出错……：" + nexterrline
                self.log.logger.error(logstr)
                if nexterrline == "" and self.shell.poll() != None:
                    break
                    # print outstr
        else:
            self.shell.kill()
            self.SelBtn32.SetLabel("Start")

    def runAnalysis(self, event):
        # redir = RedirectText(self.FileContent)

        # #设置文本框不同行信息的字体格式
        # if 'OSError' in nexterrline:
        #     self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
        # elif 'mkdir' in nexterrline:
        #     self.FileContent.SetDefaultStyle(wx.TextAttr("BLUE"))
        # else:
        #     self.FileContent.SetDefaultStyle(wx.TextAttr("BLACK"))
        # self.FileContent.AppendText(nexterrline)

        os_str = '/home/ubuntu/anaconda2/bin/python ' + self.abspath + '/analysisFile/assemble.py'  # D:\\anaconda\\
        logstr = "调用程序指令：" + os_str
        self.log.logger.debug(logstr)

        # os_str = "ipconfig"
        # self.check = subprocess.check_call(os_str)
        # print self.check
        self.shell = subprocess.Popen(os_str, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                      universal_newlines=True)
        self.FileContent.Clear()

        logstr = "开始运行分析程序……"
        self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
        self.FileContent.AppendText(logstr)
        self.FileContent.AppendText("\r\n")

        regex1 = "\^*"  # 输出匹配，只在界面显示**开头的关键信息
        regex2 = "\^*程序"  # 输出匹配，只在界面显示**开头的关键信息
        while True:
            nextline = self.shell.stdout.readline()
            if nextline == "" and self.shell.poll() != None:
                break
            # print(nextline.strip())
            # self.FileContent.Clear()
            if re.search(regex1, nextline):
                if re.search(regex2, nextline):
                    self.FileContent.SetDefaultStyle(wx.TextAttr("GREEN"))
                else:
                    self.FileContent.SetDefaultStyle(wx.TextAttr("BLACK"))
                self.FileContent.AppendText(nextline)
                wx.Yield()
                logstr = "正在分析……：" + nextline
                self.log.logger.info(logstr)
            else:
                logstr = "正在分析……：" + nextline
                self.log.logger.debug(logstr)

                # print outstr
                # self.FileContent.SetValue(outstr)
        nexterrline = self.shell.stderr.readline()
        logstr = "程序出错……：" + nexterrline
        self.log.logger.error(logstr)
        if nexterrline != "":
            self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
            self.FileContent.AppendText(nexterrline)
        while True:
            nexterrline = self.shell.stderr.readline()
            # print(nexterrline.strip())
            # self.FileContent.Clear()
            self.FileContent.AppendText(nexterrline)
            wx.Yield()
            logstr = "程序出错……：" + nexterrline
            self.log.logger.error(logstr)
            if nexterrline == "" and self.shell.poll() != None:
                break
                # print outstr

    def stopAnalysis(self, event):
        if self.shell is not None and self.shell != {} and self.shell != '':
            print "--------------"
            print type(self.shell)
            # self.shell.terminate()
            # self.shell.kill()
            # self.shell.wait()
            os.killpg(os.getpgid(self.shell.pid), signal.SIGUSR1)
            self.FileContent.SetDefaultStyle(wx.TextAttr("RED"))
            self.FileContent.AppendText("the analysis is stoped!")
            self.log.logger.error("the analysis is stoped!")

# class RedirectText(object):
#     def __init__(self,aWxTextCtrl):
#      self.out=aWxTextCtrl
#
#     def write(self,string):
#      self.out.WriteText(string)
class TabPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.frame = parent

        sizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        #self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("big_cat.jpg")
        dc.DrawBitmap(bmp, 0, 0)


# if __name__ == '__main__':
#     app = wx.App(redirect=False)
#     SiteFrame = SiteLog(None, title="Analysis")
#     # my_panel = MyPanel(SiteFrame, -1)
#     SiteFrame.Show()
#
#     # frame = wx.Frame(None, -1, '登陆窗口', size=(300, 200))
#     # my_panel = MyPanel(frame, -1)
#     app.MainLoop()

########################################################################
class MainPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent, style=wx.ALIGN_CENTER_HORIZONTAL)
        self.frame = parent
        #self.SetBackgroundColour('white')
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        #设置字体1
        font1 = wx.Font( 9, 72, 90, 90, False, "Times New Roman" )
        font1.SetPointSize(16)

        # 设置字体-button
        btnfont = wx.Font( 11, 74, 90, 90, False, "Trebuchet MS" )
        btnfont.SetPointSize(13)
        color = wx.Colour( 0, 131, 238 )

        #设置布局器
        #sizer = wx.GridBagSizer(5, 5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.SetMinSize(wx.Size(300, 480))
        sizerborder = 10

        text = wx.StaticText(self, label=u"Metagenomic Pathogen Identification Pipeline（MPIP）")
        text.SetFont(font1)
        text.SetForegroundColour(color)
        #sizer.Add(text, pos=(0, 2), span=(1, 2),flag=wx.ALL | wx.CENTER ,border=sizerborder)
        sizer.Add(text, 0, wx.CENTER| wx.TOP, sizerborder*5)

        line = wx.StaticLine(self)
        #sizer.Add(line, pos=(1, 0), span=(1, 5),flag=wx.EXPAND | wx.BOTTOM, border=sizerborder)
        sizer.Add(line, 0, wx.BOTTOM |wx.TOP | wx.EXPAND, sizerborder*2)

        self.btn1 = wx.Button(self, -1, label='Classification',size=(220, 30),style=wx.RAISED_BORDER|wx.BORDER_NONE)
        self.btn1.SetFont(btnfont)
        self.btn1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        # self.btn1.Bind(wx.EVT_ENTER_WINDOW, self.hover)
        # self.btn1.Bind(wx.EVT_LEAVE_WINDOW, self.leave)
        #sizer.Add(btn1, pos=(2, 2), span=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=sizerborder)
        sizer.Add(self.btn1, 0, wx.ALL | wx.CENTER, sizerborder)

        self.btn2 = wx.Button(self, -1, label='Pathogen characterization', size=(220, 30), style=wx.RAISED_BORDER | wx.BORDER_NONE)
        self.btn2.SetFont(btnfont)
        self.btn2.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        # self.btn2.Bind(wx.EVT_ENTER_WINDOW, self.hover)
        # self.btn2.Bind(wx.EVT_LEAVE_WINDOW, self.leave)
        # sizer.Add(btn1, pos=(2, 2), span=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=sizerborder)
        sizer.Add(self.btn2, 0, wx.ALL | wx.CENTER, sizerborder)

        self.btn3 = wx.Button(self, -1, label='Misclassification Correction', size=(220, 30), style=wx.RAISED_BORDER | wx.BORDER_NONE)
        self.btn3.SetFont(btnfont)
        self.btn3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        # self.btn3.Bind(wx.EVT_ENTER_WINDOW, self.hover)
        # self.btn3.Bind(wx.EVT_LEAVE_WINDOW, self.leave)
        # sizer.Add(btn1, pos=(2, 2), span=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=sizerborder)
        sizer.Add(self.btn3, 0, wx.ALL | wx.CENTER, sizerborder)

        self.btn4 = wx.Button(self, -1, label='Iterative assembly', size=(220, 30), style=wx.RAISED_BORDER | wx.BORDER_NONE)
        self.btn4.SetFont(btnfont)
        self.btn4.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn4.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))

        self.btn4.Bind(wx.EVT_BUTTON, self.hideFrame)
        #self.btn4.Bind(wx.EVT_ENTER_WINDOW, self.hover)
        #self.btn4.Bind(wx.EVT_LEAVE_WINDOW, self.leave)
        # sizer.Add(btn1, pos=(2, 2), span=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM,border=sizerborder)
        sizer.Add(self.btn4, 0, wx.ALL | wx.CENTER, sizerborder)


        self.SetSizer(sizer, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sizer.Fit(self)
        self.Centre()

    # ----------------------------------------------------------------------
    def hideFrame(self, event):
        """"""
        print '1111'
        self.frame.Close()
        new_frame = SiteLog(None, title="Analysis")
        new_frame.Show()

    # ----------------------------------------------------------------------
    def showFrame(self, msg):
        """
        Shows the frame and shows the message sent in the
        text control
        """
        #self.pubsubText.SetValue(msg.data)
        frame = self.GetParent()
        frame.Show()

    def hover(self,evt):
        self.btn4.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.btn4.Refresh()

        print evt

    def leave(self, evt):
        self.btn4.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn4.Refresh()

########################################################################
class MainFrame(wx.Frame):
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Analysis",size=(500,400))
        self.Centre()
        panel = MainPanel(self)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()