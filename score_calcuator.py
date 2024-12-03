# accept valid turn scores
# store string for display

class Score:

    def __init__(self):
        self.game_score = 0
        self.curr_turn_list = []
        self.curr_turn = 1
        self.frame_list = []

    def add_to_turn(self, pins_down):
        # start new frame
        # if len(self.curr_turn_list) == 2 and self.curr_turn < 10:
        #     self.frame_list.append(self.curr_turn_list)
        #     self.curr_turn_list = []
        #     self.curr_turn += 1
        # elif self.curr_turn == 10:
        #     if len(self.curr_turn_list) <= 3 or sum(self.curr_turn_list) >= 10:
        #         self.frame_list.append(self.curr_turn_list)
        #
        # self.curr_turn_list.append(pins_down)
        self.frame_list.append(pins_down)

    def return_score_str(self):
        score_str = ""
        # for frame in self.frame_list:
        #     for score in frame:
        #         if score_str != 10:
        #             score_str += str(score) + "/"
        #         else:
        #             score_str += "X"
        #     score_str += " "
        for score in self.frame_list:
            if score != 10:
                score_str += str(score) + "/"
            else:
                score_str += "X"
            score_str += " "
        return score_str

    def reset_score(self):
        self.game_score = 0
        self.curr_turn_list = []
        self.curr_turn = 1
        self.frame_list = []
        # self.score_string = ""

