# Bowling Kata

# The game consists of 10 frames.
# In each frame the player has two rolls to knock down 10 pins.
# The score for the frame is the total number of pins knocked down, plus bonuses for strikes and spares.
# A spare is when the player knocks down all 10 pins in two rolls.
# The bonus for that frame is the number of pins knocked down by the next roll.
# A strike is when the player knocks down all 10 pins on his first roll.
# The frame is then completed with a single roll. The bonus for that frame is the value of the next two rolls.
# In the tenth frame a player who rolls a spare or strike is allowed to roll the extra balls to complete the frame.
# However no more than three balls can be rolled in tenth frame.

# Write a class Game that has two methods
# void roll(int) is called each time the player rolls a ball. The argument is the number of pins knocked down.
# int score() returns the total score for that game.

# completed but untested
class Game:
    all_rolls = []
    def roll(self, pins_down):
       self.all_rolls.append(pins_down)
        
    def score(self): 
        turns = 1
        i = 0 # index
        total_score = 0
        
        # rules are same for all turns before last
        while i < len(self.all_rolls) and turns < 10:
            if turns < 10:
                if self.all_rolls[i] == 10:
                    total_score += 10
                elif self.all_rolls[i] < 10: # not last roll, so two rolls
                    total_score += self.all_rolls[i] + self.all_rolls[i+1]
                    i += 1 # skip the one added
                i += 1
            turns += 1
                    
        # last turn
        if self.all_rolls[i] == 10 or self.all_rolls[i] + self.all_rolls[i+1] == 10: # strike, so two possible rerolls
            total_score += self.all_rolls[i] + self.all_rolls[i+1] + self.all_rolls[i+2]
        else:
            total_score += self.all_rolls[i] + self.all_rolls[i+1]
        
        return total_score
            
            