#!/usr/bin/python



"""
__version__ = "$Revision: 1.9 $"
__date__ = "$Date: 2004/11/07 18:13:12 $"
"""

from PythonCard import dialog, model, timer
from types import TupleType, ListType, StringTypes, NoneType
from datetime import timedelta, time
import pprint
import os
import time
import string
import wx
    
#initializing globals

tempNumber = 0
listToggle = 0


class MulticolumnExample(model.Background):

    def on_initialize(self, event):
        """
        This method is the PythonCard equivalent to a constructor or __init__ method.
        We initialize our list of items to an empty list.
        """
        self.awayPlaying=[]
        self.homePlaying =[]
        self.awayRoster=[]
        self.awayRosterNum=[]
        self.listcache = []
        self.listcacheidx = 0
        self.opponent = ''#away team name
        self.home = ''#home team name
        self.opponentIDX = -1
        self.homeIDX = -1
        self.firstTime = 0
        self.ADDSUBTRACT = 1
        self.myTimer = timer.Timer(self.components.gameClock, -1) # create a timer
        self.timer2 = timer.Timer(self.components.theList, -1) # create a timer
        self.clockRunning = False
        self.minutes = 0
        self.seconds = 0
        self.msecs = 0
        self.GOALCONSTANT = 2
        self.homeTimes=[]
        self.awayTimes=[]
        self.timeLeft = 0
        self.homeRoster=[]
        self.homeRosterNum=[]
        
        dialog = wx.DirDialog(None, "Choose Save Location", style=1 ) 
        if dialog.ShowModal() == wx.ID_OK: 
            saveLocation = dialog.GetPath() 
        dialog.Destroy()
        self.gameStats = saveLocation+'/Game_Stats'
        if not(os.path.exists(self.gameStats)):
               os.makedirs(self.gameStats)

    def homeManually(self):#loading home roster by inserting text. Called in on_loadButton_mouseClicked function
        result = dialog.textEntryDialog(self, 
                                        'Add a player to the home team roster',
                                        'Add Player', 
                                        'Player Name')
        if result.returnedString == "Cancel":
            return
        addedPlayer = result.text
        self.homeRoster.append(addedPlayer)
        self.homeTimes.append(0)
        if result.returnedString == "Ok":
            numResult = dialog.textEntryDialog(self, 
                                    "Enter the Player's number",
                                    'A window title', 
                                    'Player Number')
        if numResult.returnedString == "Cancel":
            numResult.text = "##"
        print numResult.returnedString
        print numResult.text
        self.homeRosterNum.append(numResult.text)
        self.components.theList.columnHeadings = ['Player','Number','Goals','Assists','Shots','Groundballs','FOW','FOL','Saves','Playing','Minutes']
        for i in range(0,len(self.homeRoster)):
            self.components.theList.Append([[self.homeRoster[i],self.homeRosterNum[i],str(0),str(0),str(0),str(0),str(0),str(0),str(0),'No',str(0)]])

    def homeCSV(self):#loading home roster by loading CSV.
        #Called in on_loadButton_mouseClicked function
        wildcard = "CSV files (*.csv)|*.csv|Text files (*.txt;*.log)|*.txt;*.log|All Files (*.*)|*.*"
        result = dialog.fileDialog(self, 'Open', '', '', wildcard )
        if not result.accepted:
            return
        items = []
        for fn in result.paths:
            lines = open(fn, 'r').read().strip().split('\n')
            items.extend([x.split(',') for x in lines])
        if len(items) < 2:
            return
        self.components.theList.columnHeadings = items[0]
        tempVar = items[1:]
        self.components.theList.items = tempVar
        for i in range(0,self.components.theList.GetCount()):
            self.homeTimes.append(0)
                
    def on_loadButton_mouseClick(self, event):#loading the home team roster
    #CSV format: first column is list column headings (copy headings from button names) separated by commas
    #Next columns: PlayerName,PlayerNumber,0,0,0,0,0,0,0,No,0
        if self.homeIDX == -1:
            result = dialog.textEntryDialog(self, 
                                    'Enter Home Team Name',
                                    'Home Team', 
                                    'Team Name')
            if result.returnedString == "Cancel":
                return
            self.home = result.text
            self.components.homeLabel.text = self.home
            self.homeIDX += 1
            self.on_loadButton_mouseClick(event)
        
        elif self.homeIDX == 0:
            choice = dialog.singleChoiceDialog(self,
                                                   "How would you like to load the home team roster?",
                                                   "Load Home Roster",
                                                   ['Load CSV', 'Manually'])
            if choice.selection == 'Manually':
                self.homeManually()
                self.homeIDX = 1
            elif choice.selection == 'Load CSV':
                self.homeCSV()
                self.homeIDX = 0
            
        elif self.homeIDX > 0:
            self.homeManually()
               
    def awayManually(self):#loading away roster by inserting text. Called in on_appendButton_mouseClicked function
    #asks player name then player number
        result = dialog.textEntryDialog(self, 
                                            'Add a player to the away team roster',
                                            'Add Player', 
                                            'Player Name')
        if result.returnedString == "Cancel":
            return
        addedPlayer = result.text
        self.awayRoster.append(addedPlayer)
        self.awayTimes.append(0)
        if result.returnedString == "Ok":
            numResult = dialog.textEntryDialog(self, 
                                    "Enter the Player's number",
                                    'A window title', 
                                    'Player Number')
        if numResult.returnedString == "Cancel":
            numResult.text = "##"
        print numResult.returnedString
        print numResult.text
        self.awayRosterNum.append(numResult.text)
        self.components.otherList.columnHeadings = ['Player','Number','Goals','Assists','Shots','Groundballs','FOW','FOL','Saves','Playing','Minutes']
        for i in range(0,len(self.awayRoster)):
            self.components.otherList.Append([[self.awayRoster[i],self.awayRosterNum[i],str(0),str(0),str(0),str(0),str(0),str(0),str(0),'No',str(0)]])            
    
    def awayCSV(self):#loading away roster by loading CSV. Called in on_appendButton_mouseClicked function
    #CSV format is same as that stated in homeCSV
        wildcard = "CSV files (*.csv)|*.csv|Text files (*.txt;*.log)|*.txt;*.log|All Files (*.*)|*.*"
        result = dialog.fileDialog(self, 'Open', '', '', wildcard )
        if not result.accepted:
            return
        items = []
        for fn in result.paths:
            lines = open(fn, 'r').read().strip().split('\n')
            items.extend([x.split(',') for x in lines])
        if len(items) < 2:
            return
        self.components.otherList.columnHeadings = items[0]
        tempVar = items[1:]
        self.components.otherList.items = tempVar
        for i in range(0,self.components.otherList.GetCount()):
            self.awayTimes.append(0)

    def on_appendButton_mouseClick(self, event):#loading the away team roster 
        if self.opponentIDX == -1:
            result = dialog.textEntryDialog(self, 
                                    'Enter Away Team Name',
                                    'Away Team', 
                                    'Team Name')
            if result.returnedString == "Cancel":
                return
            self.opponent = result.text
            self.components.awayLabel.text = self.opponent
            self.opponentIDX += 1
            self.on_appendButton_mouseClick(event)
        
        elif self.opponentIDX == 0:
            choice = dialog.singleChoiceDialog(self,
                                                   "How would you like to load the away team roster?",
                                                   "Load Away Roster",
                                                   ['Load CSV', 'Manually'])
            if choice.selection == 'Manually':
                self.awayManually()
                self.opponentIDX = 1
            elif choice.selection == 'Load CSV':
                self.awayCSV()
                self.opponentIDX = 0
            
        elif self.opponentIDX > 0:
            self.awayManually()

    def on_homeClearButton_mouseClick(self, event):#clear home roster, resetting any previous loading actions
        result = dialog.messageDialog(self, 'Are you sure you want to clear the home roster?',
                          'Clear', wx.YES_NO | wx.ICON_QUESTION)
        if result.returnedString == 'Yes':
            self.components.theList.Clear()
            self.homeIDX = -1
            del self.homeRoster[:]
            del self.homeRosterNum[:]
            self.home = 'Home Team'
            self.components.homeLabel.text = self.home
    
    def on_awayClearButton_mouseClick(self, event):#clear away roster, resetting any previous loading actions
        result = dialog.messageDialog(self, 'Are you sure you want to clear the away roster?',
                          'Clear', wx.YES_NO | wx.ICON_QUESTION)
        if result.returnedString == 'Yes':
            self.components.otherList.Clear()
            self.opponentIDX = -1
            del self.awayRoster[:]
            del self.awayRosterNum[:]
            self.opponent = 'Away Team'
            self.components.awayLabel.text = self.opponent
    
    def on_exitButton_mouseClick(self, event):#exit program
        self.close()
    
    def on_goalButton_mouseClick(self, event):#when goal button clicked
        if listToggle == 0:#list toggle is switched between zero and one through the on_theList_select function and on_otherList_select. 
            tempVar = self.components.theList.items
            tempVar[tempNumber][2] = str(int(tempVar[tempNumber][2])+self.ADDSUBTRACT)#add subtract allows user to add or subtract statistic when button clicked
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][2] = str(int(tempVar[tempNumber][2])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar

    def on_assistButton_mouseClick(self, event):#when assist button clicked
        if listToggle == 0:
            tempVar = self.components.theList.items
            tempVar[tempNumber][3] = str(int(tempVar[tempNumber][3])+self.ADDSUBTRACT)
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][3] = str(int(tempVar[tempNumber][3])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar

    def on_shotButton_mouseClick(self, event):#when shot button clicked
        if listToggle == 0:
            tempVar = self.components.theList.items
            tempVar[tempNumber][4] = str(int(tempVar[tempNumber][4])+self.ADDSUBTRACT)
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][4] = str(int(tempVar[tempNumber][4])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar

    def on_groundballButton_mouseClick(self, event):#when groundball button clicked
        if listToggle == 0:
            tempVar = self.components.theList.items
            tempVar[tempNumber][5] = str(int(tempVar[tempNumber][5])+self.ADDSUBTRACT)
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][5] = str(int(tempVar[tempNumber][5])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar

    def on_faceoffWonButton_mouseClick(self, event):
        if listToggle == 0:
            tempVar = self.components.theList.items
            tempVar[tempNumber][6] = str(int(tempVar[tempNumber][6])+self.ADDSUBTRACT)
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][6] = str(int(tempVar[tempNumber][6])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar
            
    def on_faceoffLossButton_mouseClick(self, event):
        if listToggle == 0:
            tempVar = self.components.theList.items
            tempVar[tempNumber][7] = str(int(tempVar[tempNumber][7])+self.ADDSUBTRACT)
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][7] = str(int(tempVar[tempNumber][7])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar

    def on_savesButton_mouseClick(self, event):
        #This is for marking a saves statistic, not Saving the roster and Stats 
        if listToggle == 0:
            tempVar = self.components.theList.items
            tempVar[tempNumber][8] = str(int(tempVar[tempNumber][8])+self.ADDSUBTRACT)
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            tempVar[tempNumber][8] = str(int(tempVar[tempNumber][8])+self.ADDSUBTRACT)
            self.components.otherList.items = tempVar       

    def on_playButton_mouseClick(self, event):
        #Marks whether the selected player is on the field
        if listToggle == 0:
            tempVar = self.components.theList.items
            if tempVar[tempNumber][9] == 'No':
                tempVar[tempNumber][9] = 'Yes'
                self.homeTimes[tempNumber] = self.timeLeft
            else:
                tempVar[tempNumber][9] = 'No'
            self.components.theList.items = tempVar
        elif listToggle == 1:
            tempVar = self.components.otherList.items
            if tempVar[tempNumber][9] == 'No':
                tempVar[tempNumber][9] = 'Yes'
                self.awayTimes[tempNumber] = self.timeLeft
            else:
                tempVar[tempNumber][9] = 'No'
            self.components.otherList.items = tempVar
            
    def on_plusOrMinus_mouseClick(self,event):
        #button controls whether you add or subtract stats
        self.ADDSUBTRACT = self.ADDSUBTRACT*-1
        if self.components.plusOrMinus.label == '+':
            self.components.plusOrMinus.label = '-'
        else:
            self.components.plusOrMinus.label = '+'
    
    def on_saveButton_mouseClick(self, event):#Saves the current stats
        self.saveStats()

    def on_gameClock_mouseDoubleClick(self, event):#allows user to change the game clock time
        result = dialog.textEntryDialog(self, 
                                    'Enter Clock Time',
                                    'Time', 
                                    self.components.gameClock.text)
        self.minutes = int(result.text[0:result.text.index(':')])
        self.seconds = int(result.text[result.text.index(':')+1:len(result.text)])
        self.components.gameClock.text = str("%02d" % (self.minutes,))+':'+str("%02d" % (self.seconds,))
        
    def on_startClock_mouseClick(self, event):
        
        if self.components.startClock.label == 'Start':
            self.firstTime += 1
            self.clockRunning = True
            self.myTimer.Start(1000) # launch timer, to fire every 1000ms (1 seconds)
            self.timer2.Start(1000) # launch timer, to fire every 60000ms (minute)
            self.components.startClock.label = 'Stop'
            tempVar = self.components.theList.items
            for i in range(0,self.components.theList.GetCount()):
                if tempVar[i][9] == 'Yes' and self.firstTime == 1:
                    self.homeTimes[i] = self.minutes*60+self.seconds
            tempVar = self.components.otherList.items
            for i in range(0,self.components.otherList.GetCount()):#used for calculating players minutes. At start of each quarter, the minutes array is updated for the players marked on the field
                if tempVar[i][9] == 'Yes' and self.firstTime == 1:
                    self.awayTimes[i] = self.minutes*60+self.seconds
        else:
            self.clockRunning = False
            self.myTimer.Stop() # stops timer
            self.timer2.Stop() # stops timer
            self.components.startClock.label = 'Start'
            self.saveStats()
            
    def on_theList_timer(self, event):
        #updates the playing times minutes category
        tempVar = self.components.theList.items
        for i in range(0,self.components.theList.GetCount()):
            if tempVar[i][9] == 'Yes' and self.clockRunning == True and self.homeTimes[i]-self.timeLeft >= 60:
                tempVar[i][10] = str(int(tempVar[i][10]) + 1)
                self.components.theList.items = tempVar
                self.homeTimes[i] = self.timeLeft
        tempVar = self.components.otherList.items
        for i in range(0,self.components.otherList.GetCount()):
            if tempVar[i][9] == 'Yes' and self.clockRunning == True and self.awayTimes[i]-self.timeLeft >= 60:
                tempVar[i][10] = str(int(tempVar[i][10]) + 1)
                self.components.otherList.items = tempVar
                self.awayTimes[i] = self.timeLeft
        if self.timeLeft == 0:
            self.saveStats()
            self.timer2.Stop()
            self.firstTime = True

    def on_gameClock_timer(self, event):
        #reaction for the timer that updates the game clock
        self.timeLeft= self.seconds+self.minutes*60
        if self.timeLeft > 0 and self.clockRunning == True:
            self.seconds = (self.seconds-1)%60
            self.components.gameClock.text = str("%02d" % (self.minutes,))+':'+str("%02d" % (self.seconds,))
            if self.seconds == 59:
                self.minutes = (self.minutes-1)
                self.components.gameClock.text = str("%02d" % (self.minutes,))+':'+str("%02d" % (self.seconds,))
        elif self.timeLeft == 0:
            self.clockRunning = False
            self.components.startClock.label = 'Start'
            self.components.startClock.checked = False
            self.myTimer.Stop()
       
    def on_theList_itemActivated(self, event):
        #When an entry is double clicked
        base = self.components
        rows = base.theList.getStringSelection()
        if len(rows) == 0:
            return
        if not isinstance(rows[0], StringTypes):
            rows = [','.join(x) for x in rows]
        text = '\n'.join(rows)
        dlg = dialog.textEntryDialog(self, 
                                    'Edit Player Data',
                                    'Edit Data', 
                                    text)
        edit = ''
        edit = dlg.text
        edit = edit.split(',')
        tempVar = self.components.theList.items
        for i in range(0,len(self.components.theList.columnHeadings)):
            tempVar[tempNumber][i] = edit[i]
        self.components.theList.items = tempVar
     
    def on_otherList_itemActivated(self, event):
        #When an entry is double clicked
        base = self.components
        rows = base.otherList.getStringSelection()
        if len(rows) == 0:
            return
        if not isinstance(rows[0], StringTypes):
            rows = [','.join(x) for x in rows]
        text = '\n'.join(rows)
        dlg = dialog.textEntryDialog(self, 
                                    'Edit Player Data',
                                    'Edit Data', 
                                    text)
        edit = ''
        edit = dlg.text
        edit = edit.split(',')
        tempVar = self.components.otherList.items
        for i in range(0,len(self.components.otherList.columnHeadings)):
            tempVar[tempNumber][i] = edit[i]
        self.components.otherList.items = tempVar

    def on_theList_select(self, event):
        #updates the tempVar variable which is used to index the multicolumn arrays
        global tempNumber
        global listToggle
        listToggle = 0
        base = self.components
        rows = base.theList.getStringSelection()
        print rows
        #This is where the item in the list gets selected.
        if len(rows) == 0:
            return
        row = rows[0]
        if not isinstance(row, StringTypes):
            row = ' '.join(row)
        tempNumber = int(event.m_itemIndex)
 
    def on_otherList_select(self, event):
        #updates tempVar
        global tempNumber
        global listToggle
        listToggle = 1
        """When list entries are selected, display them
        (note only display first one in selection)"""
        base = self.components
        rows = base.otherList.getStringSelection()
        print rows
        """//This is where the item in the list gets selected."""
        if len(rows) == 0:
            return
        row = rows[0]
        if not isinstance(row, StringTypes):
            row = ' '.join(row)
        tempNumber = int(event.m_itemIndex)      

    def saveStats(self):
        #creates a csv of both home and away team stats
        wildcard = "CSV files (*.csv)|*.csv|Text files (*.txt;*.log)|*.txt;*.log|All Files (*.*)|*.*"
        month = time.strftime("%m")
        day = time.strftime("%d")
        year = time.strftime("%y")
        filename = str(month)+'-'+str(day)+'-'+str(year)
        
        f = open(os.path.abspath(self.gameStats+'/'+filename+'_'+self.home+'.csv'),'w')
        try:
            print f
            f.write(filename+' vs. '+self.opponent+'\n')
            f.write(self.components.theList.columnHeadings[0])
            for heading in self.components.theList.columnHeadings[1:9]:
                f.write(','+heading)
            f.write(','+self.components.theList.columnHeadings[10]+"\n")
            for i in range(0,self.components.theList.GetCount()):
                f.write(str(self.components.theList.items[i][0]))
                for j in range(1,len(self.components.theList.columnHeadings)-2):
                    f.write(','+str(self.components.theList.items[i][j]))
                f.write(','+str(self.components.theList.items[i][10])+'\n')
        finally:
            f.close()
        #Opponent Stats
        filenameAndOpponent = filename+'_'+self.opponent
        f = open(os.path.abspath(self.gameStats+'/'+filenameAndOpponent+'.csv'),'w')
        try:
            print f
            f.write(filenameAndOpponent+'\n')
            f.write(self.components.otherList.columnHeadings[0])
            for heading in self.components.otherList.columnHeadings[1:9]:
                f.write(','+heading)
            f.write(','+self.components.otherList.columnHeadings[10]+"\n")
            for i in range(0,self.components.otherList.GetCount()):
                f.write(str(self.components.otherList.items[i][0]))
                for j in range(1,len(self.components.otherList.columnHeadings)-2):
                    f.write(','+str(self.components.otherList.items[i][j]))
                f.write(','+str(self.components.otherList.items[i][10])+'\n')
        finally:
            f.close()
            
    def on_compileStatsButton_mouseClick(self, event):
        #exports compiled stats as a CSV
        playerDict = dict()
        printed = ""
        wildcard = "csv Files (*.csv)|*.csv"
        result = dialog.fileDialog(self,
                                   'Open',
                                   "",
                                   '',
                                   wildcard )
        games = result.paths
        if not(result.accepted):
            return
        for i in range(0,len(games)):
            f = open(os.path.abspath(games[i]),'r')
            try:
                lines = f.readlines()
                lines = lines[2:]
                for j in range(0,len(lines)):
                    line = lines[j].strip('\n').split(",")
                    if (line[0] in playerDict.keys()):
                        for s in range(2,10):
                            playerDict[line[0]][s] = str(int(playerDict[line[0]][s])+int(line[s]))
                    else:
                        playerDict[line[0]] = line
            finally:
                f.close()
        for key in playerDict.keys():
            playerDict[key].insert(3,str(float(playerDict[key][2])/len(games)))#goals per game
            playerDict[key].insert(5,str(float(playerDict[key][4])/len(games)))#assists per game
            playerDict[key].insert(7,str(float(playerDict[key][6])/len(games)))#shots per game
            playerDict[key].insert(9,str(float(playerDict[key][8])/len(games)))#groundballs per game
        playerNames = sorted(playerDict.keys())#sorts the keys (names of the players) so the stats can be printed in order
        printed = 'Player, Number, Total Goals, Goals per Game, Total Assists, Assists per Game, Total Shots, Shots per Game, Total Groundballs, Groundballs per Game, Total Faceoffs Won, Total Faceoffs Lost, Total Saves, Total Minutes\n'
        for k in range(0,len(playerNames)):
            printed += ','.join(playerDict[playerNames[k]])+"\n"
        result = dialog.alertDialog(self,
                                              'Statistics were saved to the compiled statistics folder.',
                                              "Compiled Statistics")

        #WRITING COMPILED STATS FILE
        v = 1 #Initialize VERSION Constant
        #Checks if file already exists
        saveDirectory = self.gameStats+"/Compiled_Stats"
        if not(os.path.exists(saveDirectory)):
               os.makedirs(saveDirectory)
        if(os.path.isfile(os.path.abspath(saveDirectory+'/Compiled Stats.csv'))):
            while(os.path.isfile(os.path.abspath(saveDirectory+'/Compiled Stats'+str(v)+'.csv'))):
                v=v+1
            filename = saveDirectory+'/Compiled Stats'+str(v)+'.csv'
            
            #creates v1,v2,etc file
            f = open(os.path.abspath(filename),'w')
            try:
                f.write(printed)
            finally:
                f.close()
        #else creates file
        else:
            f = open(os.path.abspath(saveDirectory+'/Compiled Stats.csv'),'w')
            try:
                f.write(printed)

            finally:
                f.close()
                

        
if __name__ == '__main__':
    app = model.Application(MulticolumnExample)
    app.MainLoop()
