# accept valid turn scores
# store string for display

class Score:

    def __init__(self):
        self.game_score = 0
        self.curr_turn_list = []
        self.curr_turn = 1
        self.frame_list = []
        self.game_end = False

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
        score_str = "Score: "
        total_score = 0
        for i in range(0,len(self.frame_list)):
            if self.frame_list[i] != 10:
                score_str += str(self.frame_list[i])
            elif (i+1) % 2 != 0:
                score_str += "X"
            else:
                score_str += "10 |"
                continue
            if i % 2 != 0:
                score_str += " | "
                total_score += self.frame_list[i]
            else:
                score_str += "/"
        if len(self.frame_list) == 20:
            self.game_end = True
            return "Total Score " + str(total_score)
        return score_str

    def reset_score(self):
        self.game_score = 0
        self.curr_turn_list = []
        self.curr_turn = 1
        self.frame_list = []
        # self.score_string = ""

