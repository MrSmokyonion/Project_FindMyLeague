import sys, requests, time, urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtCore

ui_form = uic.loadUiType("FindMyLeague.ui")[0]
api_key = "RGAPI-23fea51f-4a03-4857-a675-16cd64db97db"

class MyWindow(QMainWindow, ui_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Find My League")
        self.pushbtn_input.clicked.connect(self.pushbtn_input_clicked)
        self.tbox_input.returnPressed.connect(self.pushbtn_input_clicked)
        self.tbox_input.setFocus(True)

    def pushbtn_input_clicked(self):
        url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.tbox_input.text() + "?api_key=" + api_key
        r = requests.get(url)

        if self.tbox_input.text() == "":
            QMessageBox.about(self, "에러!", "소환사의 이름을 입력하세요!")
            return
        if r.status_code != 200:
            QMessageBox.about(self, "에러!", "검색을 실패했습니다!\nResponse Code: " + str(r.status_code))
            return

        self.tbox_name.setText(r.json()["name"])
        self.tbox_level.setText(str(r.json()["summonerLevel"]))

        #티어/랭크, 승리/패배 할당
        time.sleep(1)
        summonerid = r.json()["id"]
        url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerid + "?api_key=" + api_key
        r = requests.get(url)
        league_dict = r.json()[0]
        self.tbox_tier.setText(league_dict['tier'] + " " + league_dict['rank'] + " (" + str(league_dict['leaguePoints']) + "p)")
        self.tbox_win.setText(str(league_dict['wins']) + "/" + str(league_dict['losses']))

        #티어별 이미지 설정
        pixmap = QPixmap("tier/" + league_dict['tier'] + ".png")
        w = self.label_image.width()
        h = self.label_image.height()
        self.label_image.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))

        #모스트 챔피언 3개 정리
        time.sleep(1)
        url = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summonerid + "?api_key=" + api_key
        r = requests.get(url)

        i = 0
        max = 0
        if len(r.json()) < 3 : max = len(r.json())
        else: max = 3
        while i < max:
            value = r.json()[i]
            championName = ""

            url = "http://ddragon.leagueoflegends.com/cdn/9.20.1/data/en_US/champion.json"
            data = requests.get(url).json()
            for tmp in data['data']:
                if int(data['data'][tmp]['key']) == int(value['championId']):
                    championName = tmp
                    break

            url = "http://ddragon.leagueoflegends.com/cdn/9.20.1/img/champion/" + championName + ".png"
            savename = "downloadimg.png"
            urllib.request.urlretrieve(url, savename)
            pixmap = QPixmap(savename)
            w = self.label_image_cham1.width()
            h = self.label_image_cham1.height()

            if i == 0:
                self.label_level_cham1.setText("lv." + str(value['championLevel']))
                self.label_point_cham1.setText(str(value['championPoints']) + "p")
                self.label_name_cham1.setText(championName)
                self.label_image_cham1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            if i == 1:
                self.label_level_cham2.setText("lv." + str(value['championLevel']))
                self.label_point_cham2.setText(str(value['championPoints']) + "p")
                self.label_name_cham2.setText(championName)
                self.label_image_cham2.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            if i == 2:
                self.label_level_cham3.setText("lv." + str(value['championLevel']))
                self.label_point_cham3.setText(str(value['championPoints']) + "p")
                self.label_name_cham3.setText(championName)
                self.label_image_cham3.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))

            i += 1

        QMessageBox.about(self, "메세지", "검색이 완료되었습니다!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()