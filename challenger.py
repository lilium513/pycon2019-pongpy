import os

from pongpy.interfaces.team import Team
from pongpy.models.game_info import GameInfo
from pongpy.models.state import State


PLAYER_NAME = "team"

class ChallengerTeam(Team):
    def __init__(self):

        self.flag  = True
        self.flag2 = True

        self.x1 = 0 #今
        self.y1 = 0

        self.x2 = 0 #一個前
        self.y2 = 0

        self.xx1 = 0  # 今
        self.yy1 = 0

        self.xx2 = 0  # 一個前
        self.yy2 = 0

        self.delta = 0 #時間差
        self.before = 0 #前の時間

        self.delta2 = 0  # 時間差
        self.before2 = 0  # 前の時間

        self.enemy_blue_y = 0
        self.enemy_blue_y = 0


    @property
    def name(self) -> str:
        return PLAYER_NAME

    def atk_action(self, info: GameInfo, state: State) -> int:
        '''
        前衛の青色のバーをコントロールします。
        '''

        self.xx2 = self.xx1
        self.yy2 = self.yy1

        self.xx1 = state.ball_pos.x
        self.yy1 = state.ball_pos.y
        temp = state.time
        self.delta2 = temp - self.before2
        self.before2 = temp
        rate = 1
        if self.delta2 == 0:
            self.delta2 = 1
            rate = 100
        xv = (self.xx1 - self.xx2) * rate / (self.delta2)
        yv = (self.yy1 - self.yy2)* rate / (self.delta2)
        ball_dir = 1 if xv > 0 else -1
        # ボールがどっちに向かっているかを判定
        # 1が敵陣に向かっている状態

        if ball_dir == -1:
            if self.flag2:
                self.flag2 = False
                dx = state.mine_team.atk_pos.x
                rate = 1
                if xv == 0:
                    xv = 0.01
                    rate = 10
                t = (self.xx1 - dx) / (xv)  # ボールがバーの位置に来るまでの時間
                #     #先読みして良いところに居たい
                #

                if t == 0:
                    t += 0.01

                if (self.yy1 - t * yv) // (t ) < 0:

                    return  max(-info.atk_return_limit,(self.yy1 - t * yv) // (t )  )

                return min((self.yy1 - t * yv) // (t ) * 7 //7, info.atk_return_limit*7 //7)
        # shototu = #BARにぶつかる前に壁にぶつかるかを判定
        if ball_dir == 1:
            self.flag2 = True
            # if   state.mine_team.def_pos.x <state.ball_pos.x < state.mine_team.atk_pos.x:
            #     dist = state.mine_team.atk_pos.x - state.ball_pos.x
            #
            #     if xv == 0:
            #         xv += 1
            #     t = dist/xv
            #     y = t * yv
            #
            #     if y - state.mine_team.atk_pos.y >0:
            #         return -min(y - state.mine_team.atk_pos.y,info.atk_return_limit)
            #     else:
            #         return -max(y - state.mine_team.atk_pos.y, -info.atk_return_limit)


            if state.enemy_team.atk_pos.y - self.yy2 < 0:
                return max(state.enemy_team.atk_pos.y - self.yy2, -info.atk_return_limit)
            else:
                return min(state.enemy_team.atk_pos.y - self.yy2, info.atk_return_limit)

        direction = (state.ball_pos.y - state.mine_team.atk_pos.y) > 0
        return info.atk_return_limit  if direction else -(info.atk_return_limit )
    # atk_return_limit → 2

    def def_action(self, info: GameInfo, state: State) -> int:
        '''
        後衛のオレンジ色のバーをコントロールします。
        '''



        self.x2 = self.x1
        self.y2 = self.y1

        self.x1 = state.ball_pos.x
        self.y1 = state.ball_pos.y



        temp= state.time
        self.delta = temp -self.before
        self.before = temp

        rate = 1
        if self.delta ==0:
            self.delta = 0.01
        xv = (self.x1 - self.x2) * rate /(self.delta )
        yv = (self.y1 - self.y2)* rate / (self.delta)
        ball_dir = 1 if xv >= 0 else -1
        #ボールがどっちに向かっているかを判定
        #1が敵陣に向かっている状態

        if ball_dir == -1: #攻められているときは、予測して防ぐ

            #ボールの予測地点まで動いたら動かない
            if self.flag: #そこまで行ったら動かないようにFlagを立てる
                self.flag = False
        #     #反射が無いと仮定した場合
                dx = state.mine_team.def_pos.x
                rate = 1
                if xv == 0:

                    xv = 0.01

                t = (self.x1- dx) * rate/(  xv )  #ボールがバーの位置に来るまでの時間

                rate = 1
                if t == 0:
                    t = 0.01

                if (self.y1 - t * yv)* rate //(t ) < 0:
                    return info.def_return_limit
                #
                return min( (self.y1 - t * yv)* rate //(t ) ,info.def_return_limit)
       # shototu = #BARにぶつかる前に壁にぶつかるかを判定

        if ball_dir == 1:
            self.flag = True

            if state.enemy_team.atk_pos.y - self.y2 < 0:
                return max(state.enemy_team.atk_pos.y - self.y2, -info.def_return_limit)
            else:
                return min(state.enemy_team.atk_pos.y - self.y2, info.def_return_limit)


            if self.y1 < 32:
                return info.def_return_limit
            if  self.y1 < 64:

                return int (info.def_return_limit * (1-(self.y1/64)))
            if  96 <self.y1:
                -info.def_return_limit
            else:
                return -int(info.def_return_limit * (1 - ((self.y1 - 64) / 64)))


            # if state.enemy_team.atk_pos.y -self.y1 < 0:
            #     return max(state.enemy_team.atk_pos.y -self.y1,-info.def_return_limit)
            # else:
            #     return min(state.enemy_team.atk_pos.y -self.y1,info.def_return_limit)




        # if shototu

        # diff = abs(state.ball_pos.y -  state.mine_team.def_pos.x)

        # if diff < 4:
        #     return 0

        direction = (state.ball_pos.y - state.mine_team.def_pos.y) > 0
        rate  = 1
        return info.def_return_limit * rate if direction else (-info.def_return_limit) * rate

        #こっちは防御に専念