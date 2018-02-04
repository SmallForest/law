#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'深圳市三合通发精密五金制品有限公司'
import wx
import index
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "中国裁判文书网",size = (500,500))
        self.panel = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel,-1,value='',pos=(10,10),size=(470,30))
        self.button = wx.Button(self.panel,-1,label='检索',pos=(120,60),size=(260,30))
        self.button.Enable(False)
        # 绑定事件
        self.Bind(wx.EVT_TEXT,self.OnEnter,self.text)
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

    def OnClick(self,evt):
        self.button.SetLabel("检索中")
        r = index.run(self.text.GetValue())
        if r:
            self.button.SetLabel("检索完成！结果保存在%s"%r)
            self.button.Enable(False)
        else:
            self.button.SetLabel("检索失败！请重试")


    def OnEnter(self,evt):
        global z
        try:
            z = False
            print(self.text.GetValue())
            z = self.text.GetValue() != ''
        except:
            pass
        if z:
            self.button.Enable(True)
        else:
            self.button.Enable(False)
app = wx.App()
TestFrame().Show()
app.MainLoop()