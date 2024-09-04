# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def isAbbeyPresent(playHist: list, abbeyHist: list) -> bool:
    LAST_WHAT2_CHECK = 2
    if len(playHist)==len(abbeyHist) and LAST_WHAT2_CHECK<len(playHist):
        LAST_WHAT2_CHECK = [(-1*(ii+1)) for ii in range(LAST_WHAT2_CHECK)]
        LAST_WHAT2_CHECK.reverse()
        for i in LAST_WHAT2_CHECK:
            myFreq = getDistPair_freq(playHist[:i])
            myFreq = {
                playHist[i-1]+'R': myFreq[   playHist[i-1]+'R'   ],
                playHist[i-1]+'P': myFreq[   playHist[i-1]+'P'   ],
                playHist[i-1]+'S': myFreq[   playHist[i-1]+'S'   ]
            }
            oppChoice = max(myFreq, key=myFreq.get) # 'xR' xor 'xP' xor 'xS'
            oppChoice = oppChoice[-1] # 'R' xor 'P' xor 'S'
            oppChoice = rps_dic(oppChoice) # what beats it
            if abbeyHist[i]!=oppChoice:
                return False
        LAST_WHAT2_CHECK = None
        return True
    return False
def countWin(player1: list, player2: list):
    p1w, p2w  = 0, 0
    for p1, p2 in zip(player1, player2):
        p1w += 1 if (p1=='R' and p2=='S' or p1=='P' and p2=='R' or p1=='S' and p2=='P') else 0
        p2w += 1 if (p2=='R' and p1=='S' or p2=='P' and p1=='R' or p2=='S' and p1=='P') else 0
    return (p1w, p2w)
def getDistPair_freq(play_hist: list):
    out = {
        'RR': 0,
        'RP': 0,
        'RS': 0,
        'PR': 0,
        'PP': 0,
        'PS': 0,
        'SR': 0,
        'SP': 0,
        'SS': 0,
    }
    for i in range(len( play_hist )-1):
        out[ ''.join(play_hist[i:i+2]) ] +=1
    return out
def rps_dic(rps_what) -> str:
    if rps_what in ('R', 'P', 'S'):
        whatBeatsThis = {'R': 'P', 'P': 'S', 'S': 'R'} # RPS, whatBeatsItIs PSR
        # ie. whatBeatsThis['R'] = 'P'
        return whatBeatsThis[rps_what]
    return ''

def player(prev_play, opponent_history=[], thisPlayer_history=[]):
    if prev_play in ('R', 'P', 'S'):
        opponent_history.append(prev_play)
    else:
        opponent_history.clear()
        thisPlayer_history.clear()

    guess = 'P'
    # -- quincy: RPPS RRPPS RRPPS ...
    # -- abbey: max({RR:2, RP:34, RS:6, PR:8, PP:10, PS:12, SR:14, SP:18, SS:16})eg.P
    # --     due: current last(abbeysOpponent) is 'S': {SR:14, SP:18, SS:16}
    # --     max({ SR:14, SP:18, SS:16 }) is SP: 18 -> P
    # -- kris: rps_dic( prev_play )
    # -- mrugesh: rps_dic( last10mostFrequent )
    if 1<len(opponent_history):
        if 5<len(opponent_history) and (
                ''.join(opponent_history[-5:])=='RRPPS' or
                ''.join(opponent_history[-5:])=='RPPSR' or
                ''.join(opponent_history[-5:])=='PPSRR' or
                ''.join(opponent_history[-5:])=='PSRRP' or
                ''.join(opponent_history[-5:])=='SRRPP'
                ):
            last2 = "".join(opponent_history[-2:])
            guess = rps_dic(
                'R' if (last2=='PS' or last2=='SR') else
                'P' if (last2=='RR' or last2=='RP') else
                'S'
            )
            last2 = None
        elif 10<len(opponent_history):
            guess = rps_dic(rps_dic( thisPlayer_history[-1] ))

            if isAbbeyPresent(thisPlayer_history, opponent_history):
                myFreq = getDistPair_freq(thisPlayer_history)
                myFreq = {
                    thisPlayer_history[-1]+'R': myFreq[   thisPlayer_history[-1]+'R'   ],
                    thisPlayer_history[-1]+'P': myFreq[   thisPlayer_history[-1]+'P'   ],
                    thisPlayer_history[-1]+'S': myFreq[   thisPlayer_history[-1]+'S'   ]
                }
                guess = rps_dic(  rps_dic(max(myFreq, key=myFreq.get)[-1])  ) # 'R' xor 'P' xor 'S'
        else:
            guess = rps_dic( opponent_history[-1] )
    thisPlayer_history.append(guess)

    return guess
