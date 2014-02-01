{'application':{'type':'Application',
          'name':'MulticolumnExample',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMulticolumnExample',
          'title':'Lacrosse Statistics',
          'size':(929, 1000),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'MultiColumnList', 
    'name':'theList', 
    'position':(10, 50), 
    'columnHeadings':['Example List'], 
    'items':[u'Example 1', u'Example 2'], 
    'maxColumns':20, 
    'rules':1,
    'size':(700,250)
    },
{'type':'MultiColumnList', 
    'name':'otherList', 
    'position':(10, 640), 
    'columnHeadings':['Example List'], 
    'items':[u'Example 1', u'Example 2'], 
    'maxColumns':20, 
    'rules':1,
    'size':(700,250)
    },
{'type':'Button', 
    'name':'plusOrMinus', 
    'position':(825, 376), 
    'label':u'+', 
    },
{'type':'Button', 
    'name':'playButton', 
    'position':(725, 376), 
    'label':u'Playing', 
    },
{'type':'Button', 
    'name':'savesButton', 
    'position':(625, 376), 
    'label':u'Save', 
    },

{'type':'Button', 
    'name':'faceoffLossButton', 
    'position':(475, 390), 
    'label':u'Faceoff Loss', 
    },
{'type':'Button',
    'name':'faceoffWonButton', 
    'position':(475, 355), 
    'label':u'Faceoff Won', 
    },
{'type':'Button', 
    'name':'groundballButton', 
    'position':(325, 376), 
    'label':u'Groundball', 
    },

{'type':'Button', 
    'name':'shotButton', 
    'position':(225, 376), 
    'size':(80, -1), 
    'label':u'Shot', 
    },

{'type':'Button', 
    'name':'assistButton', 
    'position':(125, 376), 
    'label':u'Assist', 
    },

{'type':'Button', 
    'name':'goalButton', 
    'position':(25, 376), 
    'label':u'Goal', 
    },

{'type':'Button', 
    'name':'homeClearButton', 
    'position':(760, 120), 
    'size':(105, -1), 
    'label':u'Clear Home', 
    },
{'type':'Button', 
    'name':'awayClearButton', 
    'position':(760, 145), 
    'size':(105, -1), 
    'label':u'Clear Away', 
    },

{'type':'Button', 
    'name':'loadButton', 
    'position':(760, 70), 
    'size':(105, -1), 
    'label':u'Load Home', 
    },

{'type':'Button', 
    'name':'appendButton', 
    'position':(760, 95),
    'size':(105,-1),
    'label':u'Load Away', 
    },

{'type':'Button', 
    'name':'exitButton', 
    'position':(760, 195), 
    'size':(105, -1), 
    'label':u'Exit', 
    },

{'type':'Button', 
    'name':'saveButton', 
    'position':(760, 170), 
    'size':(105, -1), 
    'label':u'Save',
    },
{'type':'Button', 
    'name':'compileStatsButton', 
    'position':(760, 220), 
    'size':(105, -1), 
    'label':u'Compile Stats', 
    },

{'type':'StaticText', 
    'name':'gameClock', 
    'position':(100,438),
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 48},  
    'foregroundColor':(0,0,0,0), 
    'text':u'00:00', 
    },
{'type':'ToggleButton', 
    'name':'startClock', 
    'position':(120, 495), 
    'size':(100, -1), 
    'label':u'Start', 
    },
{'type':'StaticText', 
    'name':'homeLabel', 
    'position':(10,5),
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 40},  
    'foregroundColor':(0,0,0,0), 
    'text':u'Home Team', 
    },
{'type':'StaticText', 
    'name':'awayLabel', 
    'position':(10,590),
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 40},  
    'foregroundColor':(0,0,0,0), 
    'text':u'Away Team', 
    },

] # end components
} # end background
] # end backgrounds
} }
