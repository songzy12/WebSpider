import random
import copy

class Hanabi:
    SUITS=['R','G','B','Y','W']
    SUITS_WORD=['red','green','blue','yellow','white']
    
    def __init__(self,n,controller_class):
        self.clues=8
        self.mistakes=0
        self.countdown=None
        self.deck=[(s,r) for s in range(5) for r in [1,1,1,2,2,3,3,4,4,5]]
        random.shuffle(self.deck)
        self.played=[0]*5
        self.discarded=[]
        self.players=[HanabiPlayer(self,i,controller_class) for i in range(n)]
        self.hand_size=5 if n<4 else 4

    def get_info(self,p):
        return copy.deepcopy({
            'clues':self.clues,
            'mistakes':self.mistakes,
            'played':self.played,
            'discarded':self.discarded,
            'countdown':self.countdown,
            'hands':[q.hand if q!=p else None for q in self.players]})

    def display(self):
        print('Clues: %d Mistakes: %d' % (self.clues,self.mistakes))
        if self.countdown!=None: print('Countdown: %d' % self.countdown)
        print('Played: '+' '.join(['%s%d' % (Hanabi.SUITS[i],x) for i,x in enumerate(self.played)]))
        print('Discarded: '+' '.join(['%s%d' % (Hanabi.SUITS[s],r) for s,r in self.discarded]))
        print()
        for p in self.players: print('Hand of player %d: %s' % (p.index,' '.join(['%s%d' % (Hanabi.SUITS[s],r) for s,r in p.hand])))
        print()
    
    def broadcast(self,event):
        for p in self.players: p.controller.on_event(copy.deepcopy(event),self.get_info(p))
        if event['type']=='clue':
            plural=len(event['result'])>1
            print('Player %d told player %d that his/her card%s %s %s %s.' %
                  (event['player'],event['target'],'s' if plural else '', ', '.join(['#%d' % x for x in event['result']]), 'are' if plural else 'is',
                   str(event['value']) if event['kind'] else Hanabi.SUITS_WORD[event['value']]))
        elif event['type']=='play' or event['type']=='discard':
            print('Player %d %sed his/her card #%d in hand, a %s %d.' % (event['player'],event['type'],event['i'],Hanabi.SUITS_WORD[event['card'][0]],event['card'][1]))

    def play(self):
        result=None
        self.broadcast({'type':'begin'})
        for p in self.players:
            for i in range(self.hand_size): p.draw()
        self.display()
        while result==None:
            for p in self.players:
                result=p.action()
                if len(self.deck)==0:
                    if self.countdown==None: self.countdown=len(self.players)
                    else:
                        self.countdown-=1
                        if self.countdown==0: result=sum(self.played)
                self.display()
                if result!=None: break
        return result

class HanabiPlayer:
    def __init__(self,game,index,controller_class):
        self.game=game
        self.index=index
        self.controller=controller_class()
        self.hand=[]

    def draw(self):
        if len(self.game.deck)>0:
            self.hand.append(self.game.deck.pop())
            self.game.broadcast({'type':'draw','player':self.index})

    def action(self):
        a=self.controller.action(self.game.get_info(self))
        if a['type']=='clue':
            if self.game.clues==0: return 'Error: no enough clues!'
            self.game.clues-=1
            if a['target']<0 or a['kind']<0: return 'Error: malformed action!'
            if a['target']==self.index: return 'Error: cannot give clue to oneself!'
            result=[i for i,x in enumerate(self.game.players[a['target']].hand) if x[a['kind']]==a['value']]
            if len(result)==0: return 'Error: cannot give negative clue!'
            self.game.broadcast({'type':'clue','player':self.index,'target':a['target'],'kind':a['kind'],'value':a['value'],'result':result})
        elif a['type']=='play':
            if a['i']<0: return 'Error: malformed action!'
            card=self.hand.pop(a['i'])
            if card[1]==self.game.played[card[0]]+1:
                self.game.played[card[0]]+=1
                if card[1]==5 and self.game.clues<8: self.game.clues+=1
                if sum(self.game.played)==25: return 25
            else:
                self.game.discarded.append(card)
                self.game.mistakes+=1
            self.game.broadcast({'type':'play','player':self.index,'i':a['i'],'card':card})
            if self.game.mistakes==3: return 'Explosion!'
            self.draw()
        elif a['type']=='discard':
            if self.game.clues==8: return 'Error: already maximum clues!'
            if a['i']<0: return 'Error: malformed action!'
            card=self.hand.pop(a['i'])
            self.game.discarded.append(card)
            self.game.clues+=1
            self.game.broadcast({'type':'discard','player':self.index,'i':a['i'],'card':card})
            self.draw()
        else: return 'Error: unknown action!'
        
class HanabiAI:
    def __init__(self):
        self.hand=[]

    def on_event(self,event,info):
        if event['type']=='begin':
            self.n=len(info['hands'])
            self.index=info['hands'].index(None)
        elif event['type']=='draw' and event['player']==self.index:
            self.hand.append([[0,1,2,3,4],[1,2,3,4,5]])
        elif (event['type']=='play' or event['type']=='discard') and event['player']==self.index:
            self.hand.pop(event['i'])
        elif event['type']=='clue' and event['target']==self.index:
            t=event['kind']
            v=event['value']
            for i,x in enumerate(self.hand):
                if i in event['result']:
                    self.hand[i][t]=[v]
                elif v in x[t]:
                    x[t].remove(v)

    def action(self,info):
        max_score=-1
        for i,x in enumerate(self.hand):
            cnt=0
            ok_cnt=0
            for s in x[0]:
                for r in x[1]:
                    n=[0,3,2,2,2,1][r]-info['discarded'].count((s,r))
                    if info['played'][s]>=r: n-=1
                    cnt+=n
                    if info['played'][s]+1==r: ok_cnt+=n
            score=ok_cnt/cnt
            if max_score<score:
                max_score=score
                max_i=i
        if max_score>=0.5: return {'type':'play','i':max_i}
        i=(self.index+1)%self.n
        t=random.randint(0,1)
        return {'type':'clue','target':i,'kind':t,'value':info['hands'][i][random.randint(0,len(info['hands'][i])-1)][t]} if info['clues'] else {'type':'discard','i':len(self.hand)-1}

game=Hanabi(4,HanabiAI)
print('Game result: %s' % str(game.play()))
