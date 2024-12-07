# accept valid turn scores
# stores string for display

class Score:

    def __init__(self):
        self.game_score = 0
        self.roll_list = []
        self.game_end = False

    def add_to_turn(self, pins_down):
        self.roll_list.append(pins_down)

    def return_score_str(self):
        score_str = "Score: "
        total_score = 0
        next_frame = True
        max_rolls = 20
        for i in range(0, len(self.roll_list)):
            if self.roll_list[i] != 10:
                score_str += str(self.roll_list[i])
                next_frame = not next_frame
            elif next_frame:
                score_str += "X | " # strike
                continue
            else:
                score_str += " / | " # spare
                next_frame = True
                continue

            if next_frame:
                score_str += " | "
                total_score += self.roll_list[i]
            else:
                score_str += "/"

        # last frame edge cases
            # spare and extra roll
        if len(self.roll_list) == 20 and score_str[-4:] == "/ | ":
            max_rolls += 1
            # strike and two rolls
        elif len(self.roll_list) == 19 and score_str[-4:] == "X | ":
            max_rolls += 2

        # if at max_rolls, end game
        if len(self.roll_list) == max_rolls:
            self.game_end = True
            return "Total Score " + str(total_score)
        return score_str

    def reset_score(self):
        self.game_score = 0
        self.roll_list = []

