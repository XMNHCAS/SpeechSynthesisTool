import sys
import _thread as th
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_tts_form import Ui_Form
import pyttsx3


class VoiceEngine():
    '''
    tts 语音工具类
    '''

    def __init__(self):
        '''
        初始化
        '''
        # tts对象
        self.__engine = pyttsx3.init()
        # 语速
        self.__rate = 150
        # 音量
        self.__volume = 100
        # 语音ID，0为中文，1为英文
        self.__voice = 0

    @property
    def Rate(self):
        '''
        语速属性
        '''
        return self.__rate

    @Rate.setter
    def Rate(self, value):
        self.__rate = value

    @property
    def Volume(self):
        '''
        音量属性
        '''
        return self.__volume

    @Volume.setter
    def Volume(self, value):
        self.__volume = value

    @property
    def VoiceID(self):
        '''
        语音ID：0 -- 中文；1 -- 英文
        '''

        return self.__voice

    @VoiceID.setter
    def VoiceID(self, value):
        self.__voice = value

    def Say(self, text):
        '''
        播放语音
        '''
        self.__engine.setProperty('rate', self.__rate)
        self.__engine.setProperty('volume', self.__volume)
        voices = self.__engine.getProperty('voices')
        self.__engine.setProperty('voice', voices[self.__voice])

        # 保存语音文件
        # self.__engine.save_to_file(text, 'test.mp3')

        self.__engine.say(text)
        self.__engine.runAndWait()
        self.__engine.stop()


class MainWindow(QMainWindow, Ui_Form):
    '''
    窗体类
    '''

    def __init__(self, parent=None):
        '''
        初始化窗体
        '''
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 获取tts工具类实例
        self.engine = VoiceEngine()
        self.__isPlaying = False

        # 设置初始文本
        self.tbx_text.setText('床前明月光，疑似地上霜。\n举头望明月，低头思故乡。')

        # 进度条数据绑定到label中显示
        self.slider_rate.valueChanged.connect(self.setRateTextValue)
        self.slider_volumn.valueChanged.connect(self.setVolumnTextValue)

        # 设置进度条初始值
        self.slider_rate.setValue(self.engine.Rate)
        self.slider_volumn.setValue(self.engine.Volume)

        # RadioButton选择事件
        self.rbtn_zh.toggled.connect(self.onSelectVoice_zh)
        self.rbtn_en.toggled.connect(self.onSelectVoice_en)

        # 播放按钮点击事件
        self.btn_play.clicked.connect(self.onPlayButtonClick)

    def setRateTextValue(self):
        '''
        修改语速label文本值
        '''
        value = self.slider_rate.value()
        self.label_rate.setText(str(value))
        self.engine.Rate = value

    def setVolumnTextValue(self):
        '''
        修改音量label文本值
        '''
        value = self.slider_volumn.value()
        self.label_volumn.setText(str(value / 100))
        self.engine.Volume = value

    def onSelectVoice_zh(self):
        '''
        修改中文的语音配置及默认播放文本
        '''
        self.tbx_text.setText('床前明月光，疑似地上霜。\n举头望明月，低头思故乡。')
        self.engine.VoiceID = 0

    def onSelectVoice_en(self):
        '''
        修改英文的语音配置及默认的播放文本
        '''
        self.tbx_text.setText('Hello World')
        self.engine.VoiceID = 1

    def playVoice(self):
        '''
        播放
        '''

        if self.__isPlaying is not True:
            self.__isPlaying = True
            text = self.tbx_text.toPlainText()
            self.engine.Say(text)
            self.__isPlaying = False

    def onPlayButtonClick(self):
        '''
        播放按钮点击事件
        开启线程新线程播放语音，避免窗体因为语音播放而假卡死
        '''
        th.start_new_thread(self.playVoice, ())


if __name__ == "__main__":
    '''
    主函数
    '''
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
